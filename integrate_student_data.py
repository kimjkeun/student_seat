import pandas as pd
import os

print("=== 학생 데이터 통합 분석 ===")

# 1. 성적 데이터 읽기
try:
    scores_df = pd.read_csv('extract_score/reorganized_scores.csv', encoding='utf-8-sig')
    print(f"성적 데이터: {len(scores_df)}개 기록")
    print(f"성적 데이터 컬럼: {list(scores_df.columns)}")
except Exception as e:
    print(f"성적 데이터 읽기 오류: {e}")
    scores_df = pd.DataFrame()

# 2. 자리표 데이터 읽기
try:
    seating_df = pd.read_csv('seating_chart_analysis.csv', encoding='utf-8-sig')
    print(f"자리표 데이터: {len(seating_df)}개 기록")
    print(f"자리표 데이터 컬럼: {list(seating_df.columns)}")
except Exception as e:
    print(f"자리표 데이터 읽기 오류: {e}")
    seating_df = pd.DataFrame()

# 3. 이미지 데이터 읽기
try:
    images_df = pd.read_csv('image/all_class_images.csv', encoding='utf-8-sig')
    print(f"이미지 데이터: {len(images_df)}개 기록")
    print(f"이미지 데이터 컬럼: {list(images_df.columns)}")
except Exception as e:
    print(f"이미지 데이터 읽기 오류: {e}")
    images_df = pd.DataFrame()

print("\n=== 데이터 통합 시작 ===")

# 모든 학생의 기본 정보를 자리표 데이터에서 가져오기
if not seating_df.empty:
    # 자리표 데이터를 기준으로 시작
    master_df = seating_df.copy()
    
    # 학번을 표준 형식으로 변환 (30102 -> 30102)
    master_df['학번_표준'] = master_df['학번'].astype(str)
    
    print(f"기준 데이터 (자리표): {len(master_df)}명")
    
    # 성적 데이터 병합
    if not scores_df.empty:
        # 성적 데이터의 학번도 표준화
        scores_df['학번_표준'] = scores_df['학번'].astype(str)
        
        # 학번을 기준으로 병합
        master_df = master_df.merge(
            scores_df[['학번_표준', '점수']], 
            on='학번_표준', 
            how='left'
        )
        print(f"성적 데이터 병합 완료")
    
    # 이미지 데이터 병합
    if not images_df.empty:
        # 이미지 데이터의 학번도 표준화
        images_df['학번_표준'] = images_df['학번'].astype(str)
        
        # 학번을 기준으로 병합
        master_df = master_df.merge(
            images_df[['학번_표준', '파일명', '파일경로']], 
            on='학번_표준', 
            how='left'
        )
        print(f"이미지 데이터 병합 완료")
    
    # 최종 데이터 정리
    master_df = master_df.drop('학번_표준', axis=1)
    
    # 컬럼 순서 정리
    column_order = ['클래스', '학번', '이름', '행', '열', '좌석위치']
    if '점수' in master_df.columns:
        column_order.append('점수')
    if '파일명' in master_df.columns:
        column_order.extend(['파일명', '파일경로'])
    
    # 남은 컬럼들 추가
    remaining_cols = [col for col in master_df.columns if col not in column_order]
    column_order.extend(remaining_cols)
    
    master_df = master_df[column_order]
    
    # 클래스별로 정렬
    master_df = master_df.sort_values(['클래스', '학번'])
    
    print(f"\n=== 통합 결과 ===")
    print(f"총 학생 수: {len(master_df)}명")
    
    # 클래스별 통계
    print(f"\n클래스별 학생 수:")
    
    # 안전한 집계 함수 정의
    def safe_count(series):
        return series.notna().sum()
    
    agg_dict = {'학번': 'count'}
    if '점수' in master_df.columns:
        agg_dict['점수'] = safe_count
    if '파일명' in master_df.columns:
        agg_dict['파일명'] = safe_count
    
    class_stats = master_df.groupby('클래스').agg(agg_dict)
    class_stats = class_stats.rename(columns={'학번': '총인원'})
    if '점수' in class_stats.columns:
        class_stats = class_stats.rename(columns={'점수': '성적있음'})
    if '파일명' in class_stats.columns:
        class_stats = class_stats.rename(columns={'파일명': '사진있음'})
    
    print(class_stats.to_string())
    
    # 데이터 완성도 분석
    print(f"\n=== 데이터 완성도 ===")
    total_students = len(master_df)
    
    if '점수' in master_df.columns:
        students_with_scores = master_df['점수'].notna().sum()
        print(f"성적 데이터: {students_with_scores}/{total_students} ({students_with_scores/total_students*100:.1f}%)")
    
    if '파일명' in master_df.columns:
        students_with_photos = master_df['파일명'].notna().sum()
        print(f"사진 데이터: {students_with_photos}/{total_students} ({students_with_photos/total_students*100:.1f}%)")
    
    # 샘플 데이터 출력
    print(f"\n=== 샘플 통합 데이터 ===")
    print(master_df.head(10).to_string(index=False))
    
    # CSV로 저장
    master_df.to_csv('integrated_student_data.csv', index=False, encoding='utf-8-sig')
    print(f"\n통합 학생 데이터가 'integrated_student_data.csv'에 저장되었습니다.")
    
    # 누락 데이터 분석
    print(f"\n=== 누락 데이터 분석 ===")
    
    if '점수' in master_df.columns:
        missing_scores = master_df[master_df['점수'].isna()]
        if not missing_scores.empty:
            print(f"\n성적이 없는 학생 ({len(missing_scores)}명):")
            for _, student in missing_scores.iterrows():
                print(f"  클래스 {student['클래스']}: {student['학번']} {student['이름']}")
    
    if '파일명' in master_df.columns:
        missing_photos = master_df[master_df['파일명'].isna()]
        if not missing_photos.empty:
            print(f"\n사진이 없는 학생 ({len(missing_photos)}명):")
            for _, student in missing_photos.iterrows():
                print(f"  클래스 {student['클래스']}: {student['학번']} {student['이름']}")
    
    # 클래스별 상세 분석
    print(f"\n=== 클래스별 상세 분석 ===")
    for class_num in sorted(master_df['클래스'].unique()):
        class_data = master_df[master_df['클래스'] == class_num]
        
        print(f"\n클래스 {class_num} ({len(class_data)}명):")
        
        if '점수' in master_df.columns:
            scores_available = class_data['점수'].notna().sum()
            if scores_available > 0:
                avg_score = class_data['점수'].mean()
                print(f"  성적: {scores_available}/{len(class_data)}명 (평균: {avg_score:.1f}점)")
            else:
                print(f"  성적: 0/{len(class_data)}명")
        
        if '파일명' in master_df.columns:
            photos_available = class_data['파일명'].notna().sum()
            print(f"  사진: {photos_available}/{len(class_data)}명")

else:
    print("자리표 데이터가 없어 통합을 진행할 수 없습니다.")
