import pandas as pd
import os
from datetime import datetime

def generate_summary_report():
    """학생 데이터 통합 요약 보고서 생성"""
    
    print("="*80)
    print("           학생 데이터 통합 및 분석 최종 보고서")
    print("="*80)
    print(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 통합 데이터 읽기
    try:
        df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
        print(f"📊 통합 데이터 로드 완료: {len(df)}명의 학생 정보")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        return
    
    # 1. 전체 현황
    print("\n" + "="*50)
    print("1. 전체 현황")
    print("="*50)
    
    total_students = len(df)
    total_classes = df['클래스'].nunique()
    
    print(f"• 총 학생 수: {total_students:,}명")
    print(f"• 총 클래스 수: {total_classes}개 클래스")
    print(f"• 클래스별 평균 인원: {total_students/total_classes:.1f}명")
    
    # 2. 클래스별 상세 현황
    print("\n" + "="*50)
    print("2. 클래스별 상세 현황")
    print("="*50)
    
    class_summary = []
    for class_num in sorted(df['클래스'].unique()):
        class_data = df[df['클래스'] == class_num]
        
        # 기본 정보
        total_count = len(class_data)
        
        # 성적 정보
        score_count = class_data['점수'].notna().sum()
        avg_score = class_data['점수'].mean() if score_count > 0 else 0
        
        # 사진 정보
        photo_count = class_data['파일명'].notna().sum()
        
        class_summary.append({
            '클래스': f"클래스 {class_num}",
            '총인원': total_count,
            '성적보유': f"{score_count}/{total_count}",
            '성적률': f"{score_count/total_count*100:.1f}%",
            '평균점수': f"{avg_score:.1f}점" if avg_score > 0 else "N/A",
            '사진보유': f"{photo_count}/{total_count}",
            '사진률': f"{photo_count/total_count*100:.1f}%"
        })
    
    summary_df = pd.DataFrame(class_summary)
    print(summary_df.to_string(index=False))
    
    # 3. 데이터 완성도 분석
    print("\n" + "="*50)
    print("3. 데이터 완성도 분석")
    print("="*50)
    
    # 성적 데이터
    students_with_scores = df['점수'].notna().sum()
    score_completeness = students_with_scores / total_students * 100
    
    # 사진 데이터
    students_with_photos = df['파일명'].notna().sum()
    photo_completeness = students_with_photos / total_students * 100
    
    # 완전한 데이터 (성적 + 사진 모두 있음)
    complete_data = df[(df['점수'].notna()) & (df['파일명'].notna())]
    complete_count = len(complete_data)
    complete_rate = complete_count / total_students * 100
    
    print(f"• 성적 데이터 완성도: {students_with_scores}/{total_students} ({score_completeness:.1f}%)")
    print(f"• 사진 데이터 완성도: {students_with_photos}/{total_students} ({photo_completeness:.1f}%)")
    print(f"• 완전한 데이터 (성적+사진): {complete_count}/{total_students} ({complete_rate:.1f}%)")
    
    # 4. 성적 분석
    print("\n" + "="*50)
    print("4. 성적 분석")
    print("="*50)
    
    if students_with_scores > 0:
        scores = df['점수'].dropna()
        
        print(f"• 전체 평균 점수: {scores.mean():.1f}점")
        print(f"• 최고 점수: {scores.max():.1f}점")
        print(f"• 최저 점수: {scores.min():.1f}점")
        print(f"• 표준편차: {scores.std():.1f}점")
        
        # 점수 구간별 분포
        print(f"\n점수 구간별 분포:")
        bins = [0, 40, 60, 80, 100]
        labels = ['0-40점', '41-60점', '61-80점', '81-100점']
        score_dist = pd.cut(scores, bins=bins, labels=labels, include_lowest=True).value_counts()
        
        for grade, count in score_dist.items():
            percentage = count / len(scores) * 100
            print(f"  {grade}: {count}명 ({percentage:.1f}%)")
    
    # 5. 누락 데이터 상세
    print("\n" + "="*50)
    print("5. 누락 데이터 상세")
    print("="*50)
    
    # 성적 누락
    missing_scores = df[df['점수'].isna()]
    if not missing_scores.empty:
        print(f"성적이 누락된 학생 ({len(missing_scores)}명):")
        for _, student in missing_scores.iterrows():
            print(f"  • 클래스 {student['클래스']}: {student['학번']} {student['이름']}")
    else:
        print("✅ 성적 누락 없음")
    
    print()
    
    # 사진 누락
    missing_photos = df[df['파일명'].isna()]
    if not missing_photos.empty:
        print(f"사진이 누락된 학생 ({len(missing_photos)}명):")
        for _, student in missing_photos.iterrows():
            print(f"  • 클래스 {student['클래스']}: {student['학번']} {student['이름']}")
    else:
        print("✅ 사진 누락 없음")
    
    # 6. 파일 구조 요약
    print("\n" + "="*50)
    print("6. 생성된 파일 구조")
    print("="*50)
    
    files_info = [
        ("integrated_student_data.csv", "통합 학생 데이터 (메인 파일)"),
        ("seating_chart_analysis.csv", "자리표 분석 데이터"),
        ("extract_score/reorganized_scores.csv", "성적 데이터"),
        ("image/all_class_images.csv", "이미지 메타데이터"),
        ("image/class_2/", "클래스 2 학생 사진 폴더"),
        ("image/class_4/", "클래스 4 학생 사진 폴더"),
        ("image/class_5/", "클래스 5 학생 사진 폴더"),
        ("image/class_7/", "클래스 7 학생 사진 폴더"),
        ("image/class_8/", "클래스 8 학생 사진 폴더")
    ]
    
    for filename, description in files_info:
        if os.path.exists(filename):
            if os.path.isfile(filename):
                size = os.path.getsize(filename)
                print(f"📄 {filename} - {description} ({size:,} bytes)")
            else:
                try:
                    count = len(os.listdir(filename))
                    print(f"📁 {filename} - {description} ({count}개 파일)")
                except:
                    print(f"📁 {filename} - {description}")
        else:
            print(f"❌ {filename} - 파일 없음")
    
    # 7. 권장사항
    print("\n" + "="*50)
    print("7. 권장사항 및 다음 단계")
    print("="*50)
    
    recommendations = []
    
    if score_completeness < 100:
        recommendations.append(f"• 성적 데이터 누락 {total_students - students_with_scores}명 보완 필요")
    
    if photo_completeness < 100:
        recommendations.append(f"• 사진 데이터 누락 {total_students - students_with_photos}명 보완 필요")
    
    if complete_rate < 95:
        recommendations.append("• 데이터 완성도 향상을 위한 추가 작업 권장")
    
    recommendations.extend([
        "• 정기적인 데이터 백업 수행",
        "• 학생 정보 변경 시 통합 데이터 업데이트",
        "• 클래스별 성적 분석 및 리포트 생성 고려"
    ])
    
    for rec in recommendations:
        print(rec)
    
    print("\n" + "="*80)
    print("                    보고서 생성 완료")
    print("="*80)

if __name__ == "__main__":
    generate_summary_report()
