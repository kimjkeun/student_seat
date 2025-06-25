import pandas as pd

# 5행부터 35행까지 읽기
df = pd.read_excel('score.xlsx', skiprows=4, nrows=31, header=None)

print("=== 5행부터 35행까지의 데이터 ===")
print(f"데이터 크기: {df.shape[0]}행 x {df.shape[1]}열")
print()

# 각 행을 순서대로 출력
for idx, row in df.iterrows():
    print(f"행 {idx+5:2d}: ", end="")
    for col_idx, value in enumerate(row):
        if pd.notna(value):  # NaN이 아닌 값만 출력
            if isinstance(value, float):
                print(f"[{col_idx+1}]{value:.1f}", end=" ")
            else:
                print(f"[{col_idx+1}]{value}", end=" ")
    print()

print("\n=== 숫자 데이터만 추출 ===")
numeric_df = df.select_dtypes(include=['number'])
if not numeric_df.empty:
    print(f"숫자 컬럼 수: {numeric_df.shape[1]}개")
    print("통계 정보:")
    print(numeric_df.describe())
