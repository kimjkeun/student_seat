import pandas as pd
import numpy as np

def show_single_class_seating(class_num, df):
    """특정 클래스의 자리표를 깔끔하게 출력"""
    
    # 해당 클래스 학생들만 필터링
    class_students = df[df['클래스'] == class_num].copy()
    
    if class_students.empty:
        print(f"클래스 {class_num}에 학생이 없습니다.")
        return
    
    print(f"\n{'='*70}")
    print(f"                  클래스 {class_num} 자리표")
    print(f"{'='*70}")
    
    # 자리표 크기 결정
    max_row = class_students['행'].max()
    max_col = class_students['열'].max()
    
    # 자리표 배열 초기화
    seating_chart = {}
    
    # 학생 정보를 자리표에 배치
    for _, student in class_students.iterrows():
        row = student['행']
        col = student['열']
        
        # 성적 정보 처리
        if pd.notna(student['점수']):
            score_text = f"{student['점수']:.1f}점"
            score_color = "🟢" if student['점수'] >= 80 else "🟡" if student['점수'] >= 60 else "🔴"
        else:
            score_text = "성적없음"
            score_color = "⚪"
        
        # 자리 정보 구성
        seat_info = {
            '학번': student['학번'],
            '이름': student['이름'],
            '성적': score_text,
            '성적_색상': score_color,
            '사진': "📷" if pd.notna(student['파일명']) else "❌"
        }
        
        seating_chart[(row, col)] = seat_info
    
    # 클래스 기본 정보
    total_students = len(class_students)
    students_with_scores = class_students['점수'].notna().sum()
    students_with_photos = class_students['파일명'].notna().sum()
    
    print(f"👥 총 {total_students}명 | 📊 성적: {students_with_scores}명 | 📷 사진: {students_with_photos}명")
    print()
    
    # 자리표 출력 (교사 시점)
    for row in range(1, max_row + 1):
        # 빈 줄인지 확인
        has_students = any((row, col) in seating_chart for col in range(1, max_col + 1))
        
        if has_students:
            # 1줄: 학번과 성적 색상
            line1 = []
            for col in range(1, max_col + 1):
                if (row, col) in seating_chart:
                    student = seating_chart[(row, col)]
                    line1.append(f"{student['성적_색상']} {student['학번']}")
                else:
                    line1.append("          ")
            print("  " + "  |  ".join(line1))
            
            # 2줄: 이름과 사진 여부
            line2 = []
            for col in range(1, max_col + 1):
                if (row, col) in seating_chart:
                    student = seating_chart[(row, col)]
                    line2.append(f"{student['사진']} {student['이름']}")
                else:
                    line2.append("          ")
            print("  " + "  |  ".join(line2))
            
            # 3줄: 성적
            line3 = []
            for col in range(1, max_col + 1):
                if (row, col) in seating_chart:
                    student = seating_chart[(row, col)]
                    line3.append(f"   {student['성적']}")
                else:
                    line3.append("          ")
            print("  " + "  |  ".join(line3))
            
            print("  " + "-" * (12 * max_col + (max_col - 1) * 5))
    
    # 교탁 표시
    print("  " + " " * (12 * max_col // 2) + "🏫 교탁")
    print()
    
    # 범례
    print("📋 범례:")
    print("  🟢 80점 이상 (우수)  🟡 60-79점 (보통)  🔴 60점 미만 (개선필요)  ⚪ 성적없음")
    print("  📷 사진있음  ❌ 사진없음")
    print()
    
    # 클래스 통계
    print(f"📊 클래스 {class_num} 상세 통계:")
    
    # 성적 통계
    scores = class_students['점수'].dropna()
    if len(scores) > 0:
        avg_score = scores.mean()
        print(f"  • 평균 성적: {avg_score:.1f}점")
        print(f"  • 최고 성적: {scores.max():.1f}점 | 최저 성적: {scores.min():.1f}점")
        
        # 성적 구간별 분포
        excellent = len(scores[scores >= 80])
        good = len(scores[(scores >= 60) & (scores < 80)])
        needs_improvement = len(scores[scores < 60])
        
        print(f"  • 성적 분포:")
        print(f"    - 🟢 우수 (80점 이상): {excellent}명 ({excellent/len(scores)*100:.1f}%)")
        print(f"    - 🟡 보통 (60-79점): {good}명 ({good/len(scores)*100:.1f}%)")
        print(f"    - 🔴 개선필요 (60점 미만): {needs_improvement}명 ({needs_improvement/len(scores)*100:.1f}%)")
    else:
        print("  • 성적 데이터 없음")
    
    # 우수 학생과 개선 필요 학생
    if len(scores) > 0:
        top_students = class_students[class_students['점수'] >= 80]['이름'].tolist()
        low_students = class_students[class_students['점수'] < 60]['이름'].tolist()
        
        if top_students:
            print(f"  • 🌟 우수 학생: {', '.join(top_students)}")
        if low_students:
            print(f"  • 💪 개선 필요 학생: {', '.join(low_students)}")
    
    return class_students

def show_student_details(class_num, df):
    """클래스별 학생 상세 정보"""
    
    class_students = df[df['클래스'] == class_num].copy()
    
    if class_students.empty:
        return
    
    print(f"\n📝 클래스 {class_num} 학생 명단 (좌석 순서)")
    print("-" * 70)
    
    # 행, 열 순으로 정렬
    class_students = class_students.sort_values(['행', '열'])
    
    for idx, (_, student) in enumerate(class_students.iterrows(), 1):
        score_text = f"{student['점수']:.1f}점" if pd.notna(student['점수']) else "성적없음"
        photo_text = "📷" if pd.notna(student['파일명']) else "❌"
        
        print(f"{idx:2d}. {student['학번']} {student['이름']:4s} | 좌석({student['행']},{student['열']}) | {score_text:8s} | {photo_text}")

def main():
    """메인 함수 - 클래스별로 선택해서 보기"""
    
    print("="*70)
    print("                클래스별 자리표 뷰어")
    print("="*70)
    
    # 통합 데이터 읽기
    try:
        df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
        print(f"✅ 데이터 로드 완료: {len(df)}명의 학생 정보")
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        return
    
    # 클래스 목록 확인
    classes = sorted(df['클래스'].unique())
    print(f"📚 사용 가능한 클래스: {classes}")
    
    while True:
        print(f"\n{'='*70}")
        print("클래스를 선택하세요:")
        for i, class_num in enumerate(classes, 1):
            student_count = len(df[df['클래스'] == class_num])
            print(f"  {i}. 클래스 {class_num} ({student_count}명)")
        print(f"  0. 전체 클래스 보기")
        print(f"  q. 종료")
        
        choice = input("\n선택 (번호 입력): ").strip()
        
        if choice.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        elif choice == '0':
            # 전체 클래스 보기
            for class_num in classes:
                show_single_class_seating(class_num, df)
                show_student_details(class_num, df)
                input("\n다음 클래스를 보려면 Enter를 누르세요...")
        else:
            try:
                class_idx = int(choice) - 1
                if 0 <= class_idx < len(classes):
                    selected_class = classes[class_idx]
                    show_single_class_seating(selected_class, df)
                    show_student_details(selected_class, df)
                else:
                    print("❌ 잘못된 선택입니다.")
            except ValueError:
                print("❌ 숫자를 입력해주세요.")

if __name__ == "__main__":
    # 먼저 클래스 2를 예시로 보여주기
    try:
        df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
        print("📖 클래스 2 자리표 예시:")
        show_single_class_seating(2, df)
        show_student_details(2, df)
        
        print(f"\n{'='*70}")
        print("💡 전체 클래스를 보려면 main() 함수를 실행하세요!")
        print("   예: python show_class_seating.py 후 대화형 모드 사용")
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        main()
