import pandas as pd

# 5행부터 35행까지 읽기
df = pd.read_excel('score.xlsx', skiprows=4, nrows=31, header=None)

print("=== 5행부터 35행까지의 데이터 ===")
print(f"데이터 크기: {df.shape[0]}행 x {df.shape[1]}열")

# CSV로 저장
df.to_csv('extracted_data.csv', index=False, encoding='utf-8-sig')
print("데이터를 'extracted_data.csv'로 저장했습니다.")

# 처음 10행만 출력
print("\n=== 처음 10행 미리보기 ===")
for i in range(min(10, len(df))):
    row_data = []
    for j, value in enumerate(df.iloc[i]):
        if pd.notna(value):
            row_data.append(f"열{j+1}:{value}")
    print(f"행{i+5}: {' | '.join(row_data)}")

# 헤더 행 확인 (5행)
print("\n=== 헤더 정보 (5행) ===")
header_row = df.iloc[0]
for i, value in enumerate(header_row):
    if pd.notna(value):
        print(f"열{i+1}: {value}")

# 학생 데이터 샘플 (6-10행)
print("\n=== 학생 데이터 샘플 (6-10행) ===")
for i in range(1, min(6, len(df))):
    student_data = []
    for j, value in enumerate(df.iloc[i]):
        if pd.notna(value):
            student_data.append(f"{value}")
    print(f"학생{i}: {' | '.join(student_data)}")
