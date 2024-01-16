from pykrx import stock
import pandas as pd
import os

# 데이터를 저장할 빈 DataFrame 생성
df = pd.DataFrame()

# 날짜 범위 설정
start = "20200101"
end = "20231231"

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

    # 일자별 eps / per 추가
    date_fd = stock.get_market_fundamental(date)

    # date_data와 date_fd 데이터프레임을 '종목코드'를 기준으로 합치기
    df = pd.concat([df, pd.merge(date_data, date_fd, how='inner', on='티커').reset_index(drop=True)])

    # 한 달이 지나면 데이터를 해당 월의 CSV 파일로 저장
    if date.month != (date + pd.DateOffset(days=1)).month:
        # 폴더 경로 생성
        folder_path = f"data/{date.year}/{date.strftime('%m')}"
        os.makedirs("data", exist_ok=True)  # data폴더가 없으면 생성
        os.makedirs(folder_path, exist_ok=True)  # 폴더가 없으면 생성
        stock_file = os.path.join(folder_path, f"stock_{date_str}.csv")

        # 데이터를 CSV 파일로 저장
        df.to_csv(stock_file, encoding='utf-8-sig', index=False)  # utf-8-sig는 엑셀에서 한글 깨짐 방지

        print(f"{stock_file} 파일이 성공적으로 저장되었습니다.")

        # 다음 달을 위해 DataFrame 초기화
        df = pd.DataFrame()
