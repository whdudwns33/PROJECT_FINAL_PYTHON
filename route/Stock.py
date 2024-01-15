from pykrx import stock
import pandas as pd

# 날짜 범위 설정
start = "20230901"
end = "20240110"

# 데이터를 저장할 빈 DataFrame 생성
df = pd.DataFrame()

# 지정된 범위 내의 각 날짜에 대해 루프를 돌면서 데이터를 가져오기
for date in pd.date_range(start, end):
    date_str = date.strftime("%Y%m%d")
    date_data = stock.get_market_ohlcv(date_str, market="ALL")
    # 날짜 추가
    date_data["날짜"] = date_str
    # 인덱스(티커) 값 추가
    date_data["종목코드"] = date_data.index.astype(str).tolist()
    # 인덱스(티커) 값을 뽑아내서 종목의 이름으로 변환
    date_data["종목명"] = date_data.index.map(lambda ticker: stock.get_market_ticker_name(ticker))

    # '티커' 컬럼을 일반적인 열로 유지하고, 독립적인 순차적인 인덱스를 사용
    df = pd.concat([df, date_data.reset_index(drop=True)], ignore_index=True)

# CSV 파일로 저장 (index=True로 설정하여 독립적인 순차적인 인덱스를 저장함)

stock_file = "stock_{}_{}.csv".format(start, end)
df.to_csv(stock_file, encoding='utf-8-sig', index=True)  # utf-8-sig는 엑셀에서 한글 깨짐 방지

print(f"{stock_file} 파일이 성공적으로 저장되었습니다.")