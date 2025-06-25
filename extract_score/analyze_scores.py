import pandas as pd

# 5행부터 35행까지 읽기 (학생 성적 데이터)
df = pd.read_excel('score.xlsx', skiprows=4, nrows=31, header=None)

# 컬럼명 설정
df.columns = ['학생번호', '1반', '2반', '3반', '4반', '5반', '6반', '7반', '8반', '9반', '열11', '열12', '열13']

# 첫 번째 행은 헤더이므로 제거하고 실제 데이터만 사용
student_data = df.iloc[1:].copy()
student_data = student_data.iloc[:, :10]  # 처음 10개 열만 사용 (학생번호 + 9개 반)

print("=== 학생별 반 수강 현황 및 성적 ===")
print(f"총 학생 수: {len(student_data)}명")
print(f"총 반 수: 9개 반")
print()

# 각 학생의 수강 현황 분석
print("=== 학생별 수강 반 수 및 평균 성적 ===")
for idx, row in student_data.iterrows():
    student_num = int(row['학생번호']) if pd.notna(row['학생번호']) else idx
    
    # 수강한 반과 성적 추출
    grades = []
    classes_taken = []
    
    for class_num in range(1, 10):
        grade = row[f'{class_num}반']
        if pd.notna(grade):
            grades.append(grade)
            classes_taken.append(f'{class_num}반')
    
    if grades:
        avg_grade = sum(grades) / len(grades)
        print(f"학생 {student_num:2d}: {len(grades)}개 반 수강, 평균 {avg_grade:.1f}점 - {', '.join(classes_taken)}")
    else:
        print(f"학생 {student_num:2d}: 수강 반 없음")

print("\n=== 반별 수강 학생 수 및 평균 성적 ===")
for class_num in range(1, 10):
    class_col = f'{class_num}반'
    class_grades = student_data[class_col].dropna()
    
    if len(class_grades) > 0:
        avg_grade = class_grades.mean()
        max_grade = class_grades.max()
        min_grade = class_grades.min()
        print(f"{class_num}반: {len(class_grades)}명 수강, 평균 {avg_grade:.1f}점 (최고 {max_grade:.1f}, 최저 {min_grade:.1f})")
    else:
        print(f"{class_num}반: 수강 학생 없음")

print("\n=== 전체 통계 ===")
all_grades = []
for class_num in range(1, 10):
    class_grades = student_data[f'{class_num}반'].dropna()
    all_grades.extend(class_grades.tolist())

if all_grades:
    print(f"전체 성적 개수: {len(all_grades)}개")
    print(f"전체 평균: {sum(all_grades)/len(all_grades):.1f}점")
    print(f"최고 점수: {max(all_grades):.1f}점")
    print(f"최저 점수: {min(all_grades):.1f}점")

# 수강 패턴 분석
print("\n=== 수강 패턴 분석 ===")
enrollment_counts = {}
for idx, row in student_data.iterrows():
    count = 0
    for class_num in range(1, 10):
        if pd.notna(row[f'{class_num}반']):
            count += 1
    
    if count in enrollment_counts:
        enrollment_counts[count] += 1
    else:
        enrollment_counts[count] = 1

for count, students in sorted(enrollment_counts.items()):
    print(f"{count}개 반 수강: {students}명")
