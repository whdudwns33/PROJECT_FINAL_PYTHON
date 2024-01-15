from pykrx import stock
import pandas as pd

start = "20231230"
end = "20231231"

df = pd.DataFrame()
for date in pd.date_range(start, end):
    date_str = date.strftime("%Y%m%d")
    date_data = stock.get_market_ohlcv(date_str, market="ALL")
    # 날짜 추가
    date_data["날짜"] = date_str
    # 인덱스(티커) 값 추가
    date_data["종목코드"] = date_data.index.astype(str).tolist()
    # 인덱스(티커) 값을 뽑아내서 종목의 이름으로 변환
    date_data["종목명"] = date_data.index.map(lambda ticker: stock.get_market_ticker_name(ticker))
    # print("date_data",date_data)
    date_cap = stock.get_market_cap(date)
    print("date_cap",date_cap)

    # 일자별 eps / per 추가
    date_fd = stock.get_market_fundamental(date)
    # print("date_fd", date_fd)
    # date_data와 date_fd 데이터프레임을 '종목코드'를 기준으로 합치기
    merged_fd = pd.merge(date_data, date_fd, how='inner', on='티커')
    # merged_cap = pd.merge(merged_fd, date_cap, how='inner', on='티커')
    df = pd.concat([df, merged_fd.reset_index(drop=True)], ignore_index=True)

    # 불필요한 열 제거 (예: '티커' 열은 이미 '종목코드'로 합쳤으므로 제거)
    # merged_df.drop(['티커'], axis=1, inplace=True)

    print(df)

# print(df)