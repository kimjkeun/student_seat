import pandas as pd
import numpy as np

try:
    # 엑셀 파일 읽기
    df = pd.read_excel('score.xlsx', header=None)
    
    print("=== 엑셀 파일 기본 정보 ===")
    print(f"파일 크기: {df.shape[0]}행 x {df.shape[1]}열")
    print()
    
    print("=== 전체 데이터 ===")
    # NaN 값을 빈 문자열로 대체하여 출력
    df_display = df.fillna('')
    
    for idx, row in df_display.iterrows():
        # 빈 값이 아닌 셀만 출력
        non_empty = [(i, val) for i, val in enumerate(row) if val != '']
        if non_empty:
            print(f"행 {idx+1:2d}: ", end="")
            for col_idx, value in non_empty:
                print(f"[{col_idx+1}]{value}", end=" ")
            print()
    
    print("\n=== 데이터 타입 분석 ===")
    for col in df.columns:
        non_null_data = df[col].dropna()
        if len(non_null_data) > 0:
            data_types = set(type(x).__name__ for x in non_null_data)
            print(f"열 {col+1}: {len(non_null_data)}개 값, 타입: {data_types}")
    
    print("\n=== 숫자 데이터 요약 ===")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(df[numeric_cols].describe())
    else:
        print("숫자 데이터가 없습니다.")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")
