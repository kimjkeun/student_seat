import pandas as pd
import numpy as np
import os

def create_class_seating_chart(class_num, df):
    """특정 클래스의 자리표를 생성"""
    
    # 해당 클래스 학생들만 필터링
    class_students = df[df['클래스'] == class_num].copy()
    
    if class_students.empty:
        print(f"클래스 {class_num}에 학생이 없습니다.")
        return
    
    print(f"\n{'='*80}")
    print(f"                    클래스 {class_num} 자리표")
    print(f"{'='*80}")
    
    # 자리표 크기 결정 (행, 열의 최대값 기준)
    max_row = class_students['행'].max()
    max_col = class_students['열'].max()
    
    # 자리표 배열 초기화
    seating_chart = {}
    
    # 학생 정보를 자리표에 배치
    for _, student in class_students.iterrows():
        row = student['행']
        col = student['열']
        
        # 성적 정보 처리
        score_text = f"{student['점수']:.1f}점" if pd.notna(student['점수']) else "성적없음"
        
        # 자리 정보 구성
        seat_info = {
            '학번': student['학번'],
            '이름': student['이름'],
            '성적': score_text,
            '사진': "있음" if pd.notna(student['파일명']) else "없음"
        }
        
        seating_chart[(row, col)] = seat_info
    
    # 자리표 출력 (교사 시점)
    print(f"총 {len(class_students)}명 | 성적 보유: {class_students['점수'].notna().sum()}명 | 사진 보유: {class_students['파일명'].notna().sum()}명")
    print()
    
    # 행별로 출력
    for row in range(1, max_row + 1):
        # 각 행의 학생 정보 수집
        row_students = []
        for col in range(1, max_col + 1):
            if (row, col) in seating_chart:
                student = seating_chart[(row, col)]
                row_students.append(student)
            else:
                row_students.append(None)
        
        # 행 출력 (3줄로 구성: 학번, 이름, 성적)
        if any(student is not None for student in row_students):
            # 1줄: 학번
            line1 = []
            for student in row_students:
                if student:
                    line1.append(f"{student['학번']:^12}")
                else:
                    line1.append("            ")
            print("  " + " | ".join(line1))
            
            # 2줄: 이름
            line2 = []
            for student in row_students:
                if student:
                    line2.append(f"{student['이름']:^12}")
                else:
                    line2.append("            ")
            print("  " + " | ".join(line2))
            
            # 3줄: 성적
            line3 = []
            for student in row_students:
                if student:
                    line3.append(f"{student['성적']:^12}")
                else:
                    line3.append("            ")
            print("  " + " | ".join(line3))
            
            print("  " + "-" * (13 * max_col + (max_col - 1) * 3))
    
    # 교탁 표시
    print("  " + " " * (13 * max_col // 2 - 2) + "교탁")
    print()
    
    # 클래스 통계
    print(f"📊 클래스 {class_num} 통계:")
    
    # 성적 통계
    scores = class_students['점수'].dropna()
    if len(scores) > 0:
        print(f"  • 평균 성적: {scores.mean():.1f}점")
        print(f"  • 최고 성적: {scores.max():.1f}점")
        print(f"  • 최저 성적: {scores.min():.1f}점")
        
        # 성적 구간별 분포
        high_scores = len(scores[scores >= 80])
        mid_scores = len(scores[(scores >= 60) & (scores < 80)])
        low_scores = len(scores[scores < 60])
        
        print(f"  • 성적 분포: 우수(80점 이상) {high_scores}명, 보통(60-79점) {mid_scores}명, 개선필요(60점 미만) {low_scores}명")
    else:
        print("  • 성적 데이터 없음")
    
    # 자리 배치 특이사항
    front_row_students = class_students[class_students['행'] <= 2]
    back_row_students = class_students[class_students['행'] >= max_row - 1]
    
    if len(front_row_students) > 0:
        print(f"  • 앞자리 학생 ({len(front_row_students)}명): {', '.join(front_row_students['이름'].tolist())}")
    
    if len(back_row_students) > 0:
        print(f"  • 뒷자리 학생 ({len(back_row_students)}명): {', '.join(back_row_students['이름'].tolist())}")
    
    return class_students

def create_detailed_student_list(class_num, df):
    """클래스별 상세 학생 명단 생성"""
    
    class_students = df[df['클래스'] == class_num].copy()
    
    if class_students.empty:
        return
    
    print(f"\n📋 클래스 {class_num} 상세 학생 명단")
    print("-" * 80)
    
    # 학번순으로 정렬
    class_students = class_students.sort_values('학번')
    
    print(f"{'번호':>3} {'학번':>6} {'이름':>8} {'좌석':>8} {'성적':>8} {'사진':>6}")
    print("-" * 50)
    
    for idx, (_, student) in enumerate(class_students.iterrows(), 1):
        score_text = f"{student['점수']:.1f}" if pd.notna(student['점수']) else "없음"
        photo_text = "있음" if pd.notna(student['파일명']) else "없음"
        seat_text = f"({student['행']},{student['열']})"
        
        print(f"{idx:>3} {student['학번']:>6} {student['이름']:>8} {seat_text:>8} {score_text:>8} {photo_text:>6}")

def main():
    """메인 함수"""
    
    print("="*80)
    print("                    클래스별 자리표 생성기")
    print("="*80)
    
    # 통합 데이터 읽기
    try:
        df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
        print(f"✅ 통합 데이터 로드 완료: {len(df)}명의 학생 정보")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        return
    
    # 클래스 목록 확인
    classes = sorted(df['클래스'].unique())
    print(f"📚 발견된 클래스: {classes}")
    
    # 각 클래스별 자리표 생성
    for class_num in classes:
        # 자리표 생성
        class_data = create_class_seating_chart(class_num, df)
        
        # 상세 명단 생성
        create_detailed_student_list(class_num, df)
        
        # 클래스별 CSV 파일 저장
        if class_data is not None and not class_data.empty:
            filename = f'class_{class_num}_seating_chart.csv'
            
            # 자리표용 데이터 정리
            output_data = class_data[['학번', '이름', '행', '열', '좌석위치', '점수', '파일명']].copy()
            output_data['성적_표시'] = output_data['점수'].apply(
                lambda x: f"{x:.1f}점" if pd.notna(x) else "성적없음"
            )
            output_data['사진_여부'] = output_data['파일명'].apply(
                lambda x: "있음" if pd.notna(x) else "없음"
            )
            
            output_data.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"💾 클래스 {class_num} 자리표가 '{filename}'에 저장되었습니다.")
    
    print(f"\n{'='*80}")
    print("                    자리표 생성 완료!")
    print(f"{'='*80}")
    print("💡 사용법:")
    print("  • 각 자리표에서 학번, 이름, 성적을 함께 확인하여 학습하세요")
    print("  • 앞자리/뒷자리 학생들을 우선적으로 기억해보세요")
    print("  • 성적이 높은 학생들과 개선이 필요한 학생들을 구분하여 기억하세요")
    print("  • 사진이 있는 학생들은 얼굴과 함께 기억하세요")

if __name__ == "__main__":
    main()
