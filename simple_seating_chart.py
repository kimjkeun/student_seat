import pandas as pd

def create_simple_seating_chart(class_num):
    """클래스별 간단한 자리표 생성"""
    
    # 데이터 로드
    df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
    
    # 해당 클래스 학생들만 필터링
    class_students = df[df['클래스'] == class_num].copy()
    
    if class_students.empty:
        print(f"클래스 {class_num}에 학생이 없습니다.")
        return
    
    print(f"\n{'='*60}")
    print(f"                클래스 {class_num} 자리표")
    print(f"{'='*60}")
    
    # 자리표 크기 결정
    max_row = class_students['행'].max()
    max_col = class_students['열'].max()
    
    print(f"총 {len(class_students)}명 학생")
    print()
    
    # 자리표 생성
    seating_grid = {}
    for _, student in class_students.iterrows():
        row, col = student['행'], student['열']
        
        # 성적 표시
        if pd.notna(student['점수']):
            score = student['점수']
            if score >= 80:
                score_mark = "★"  # 우수
            elif score >= 60:
                score_mark = "○"  # 보통
            else:
                score_mark = "△"  # 개선필요
        else:
            score_mark = "?"  # 성적없음
        
        # 사진 표시
        photo_mark = "📷" if pd.notna(student['파일명']) else "❌"
        
        seating_grid[(row, col)] = {
            'name': student['이름'],
            'id': student['학번'],
            'score': student['점수'] if pd.notna(student['점수']) else 0,
            'score_mark': score_mark,
            'photo_mark': photo_mark
        }
    
    # 자리표 출력
    for row in range(1, max_row + 1):
        # 이름 줄
        name_line = []
        score_line = []
        
        for col in range(1, max_col + 1):
            if (row, col) in seating_grid:
                student = seating_grid[(row, col)]
                name_line.append(f"{student['name']:^8}")
                score_text = f"{student['score_mark']}{student['score']:.0f}" if student['score'] > 0 else f"{student['score_mark']}--"
                score_line.append(f"{score_text:^8}")
            else:
                name_line.append("        ")
                score_line.append("        ")
        
        print("  " + " | ".join(name_line))
        print("  " + " | ".join(score_line))
        print("  " + "-" * (9 * max_col + (max_col - 1) * 3))
    
    print(f"{'교탁':^{9 * max_col + (max_col - 1) * 3}}")
    print()
    
    # 범례
    print("📋 범례: ★우수(80+점) ○보통(60-79점) △개선필요(60점미만) ?성적없음")
    print("        📷사진있음 ❌사진없음")
    print()
    
    # 통계
    scores = class_students['점수'].dropna()
    if len(scores) > 0:
        print(f"📊 성적 통계:")
        print(f"   평균: {scores.mean():.1f}점")
        print(f"   최고: {scores.max():.1f}점 | 최저: {scores.min():.1f}점")
        
        excellent = len(scores[scores >= 80])
        good = len(scores[(scores >= 60) & (scores < 80)])
        needs_improvement = len(scores[scores < 60])
        
        print(f"   우수: {excellent}명 | 보통: {good}명 | 개선필요: {needs_improvement}명")
    
    print()
    
    # 학생 명단 (성적순)
    print("📝 학생 명단 (성적순):")
    sorted_students = class_students.sort_values('점수', ascending=False, na_position='last')
    
    for i, (_, student) in enumerate(sorted_students.iterrows(), 1):
        score_text = f"{student['점수']:.1f}점" if pd.notna(student['점수']) else "성적없음"
        photo_text = "📷" if pd.notna(student['파일명']) else "❌"
        print(f"  {i:2d}. {student['이름']:4s} ({student['학번']}) - {score_text:8s} {photo_text}")

def show_all_classes():
    """모든 클래스 자리표 보기"""
    
    df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
    classes = sorted(df['클래스'].unique())
    
    print("="*60)
    print("              전체 클래스 자리표")
    print("="*60)
    
    for class_num in classes:
        create_simple_seating_chart(class_num)
        input("다음 클래스를 보려면 Enter를 누르세요...")

if __name__ == "__main__":
    # 사용자 선택
    try:
        df = pd.read_csv('integrated_student_data.csv', encoding='utf-8-sig')
        classes = sorted(df['클래스'].unique())
        
        print("="*60)
        print("              클래스 자리표 생성기")
        print("="*60)
        print(f"사용 가능한 클래스: {classes}")
        print()
        
        while True:
            print("선택하세요:")
            print("1. 특정 클래스 보기")
            print("2. 모든 클래스 보기")
            print("3. 종료")
            
            choice = input("\n번호 입력: ").strip()
            
            if choice == "1":
                class_num = input(f"클래스 번호 입력 {classes}: ")
                try:
                    class_num = int(class_num)
                    if class_num in classes:
                        create_simple_seating_chart(class_num)
                    else:
                        print("❌ 존재하지 않는 클래스입니다.")
                except ValueError:
                    print("❌ 숫자를 입력해주세요.")
            
            elif choice == "2":
                show_all_classes()
            
            elif choice == "3":
                print("프로그램을 종료합니다.")
                break
            
            else:
                print("❌ 1, 2, 3 중에서 선택해주세요.")
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        # 기본으로 클래스 2 보여주기
        create_simple_seating_chart(2)
