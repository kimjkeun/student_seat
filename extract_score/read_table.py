import pandas as pd

# 5행부터 35행까지 읽기 (pandas는 0-based이므로 skiprows=4, nrows=31)
df = pd.read_excel('score.xlsx', skiprows=4, nrows=31, header=None)

print("=== 5행부터 35행까지의 데이터 ===")
print(f"데이터 크기: {df.shape[0]}행 x {df.shape[1]}열")
print()

# 컬럼명을 숫자로 설정
df.columns = [f'열{i+1}' for i in range(df.shape[1])]

# 전체 데이터 출력
print("=== 전체 테이블 ===")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 20)

print(df.to_string(index=True))

print("\n=== 데이터 타입 정보 ===")
print(df.dtypes)

print("\n=== 결측값 정보 ===")
print(df.isnull().sum())

print("\n=== 숫자 데이터 통계 ===")
numeric_df = df.select_dtypes(include=['number'])
if not numeric_df.empty:
    print(numeric_df.describe())
else:
    print("숫자 데이터가 없습니다.")
