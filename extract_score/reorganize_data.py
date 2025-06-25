import pandas as pd

# 5행부터 35행까지 읽기 (학생 성적 데이터)
df = pd.read_excel('score.xlsx', skiprows=4, nrows=31, header=None)

# 컬럼명 설정
df.columns = ['학생번호', '1반', '2반', '3반', '4반', '5반', '6반', '7반', '8반', '9반', '열11', '열12', '열13']

# 첫 번째 행은 헤더이므로 제거하고 실제 데이터만 사용
student_data = df.iloc[1:].copy()
student_data = student_data.iloc[:, :10]  # 처음 10개 열만 사용 (학생번호 + 9개 반)

# 새로운 형식으로 데이터 정리
reorganized_data = []

print("=== 데이터 정리 중... ===")

for idx, row in student_data.iterrows():
    student_num = int(row['학생번호']) if pd.notna(row['학생번호']) else idx
    
    # 각 반에 대해 점수가 있는 경우만 추가
    for class_num in range(1, 10):
        grade = row[f'{class_num}반']
        if pd.notna(grade):  # 점수가 있는 경우만
            # 학번 생성: 3AABB 형식 (AA는 반, BB는 번호)
            student_id = f"3{class_num:02d}{student_num:02d}"
            
            reorganized_data.append({
                '반': class_num,
                '번호': student_num,
                '학번': student_id,
                '점수': grade
            })

# DataFrame으로 변환
result_df = pd.DataFrame(reorganized_data)

print(f"총 {len(result_df)}개의 성적 데이터가 정리되었습니다.")
print()

# 결과 출력
print("=== 정리된 데이터 (처음 20개) ===")
print(result_df.head(20).to_string(index=False))

if len(result_df) > 20:
    print(f"\n... (총 {len(result_df)}개 중 처음 20개만 표시)")

# CSV로 저장
result_df.to_csv('reorganized_scores.csv', index=False, encoding='utf-8-sig')
print(f"\n데이터가 'reorganized_scores.csv' 파일로 저장되었습니다.")

# 반별 통계
print("\n=== 반별 데이터 개수 ===")
class_counts = result_df['반'].value_counts().sort_index()
for class_num, count in class_counts.items():
    print(f"{class_num}반: {count}개")

print("\n=== 점수 통계 ===")
print(f"평균 점수: {result_df['점수'].mean():.1f}점")
print(f"최고 점수: {result_df['점수'].max():.1f}점")
print(f"최저 점수: {result_df['점수'].min():.1f}점")
