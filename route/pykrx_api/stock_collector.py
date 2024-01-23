from pykrx import stock
from datetime import datetime
from calendar import monthrange
import pandas as pd
import os
from common.logger_config import config_logger
from common.constant import LOGGER_PATH, DATA_SAVE_PATH

# 로거 설정
logger = config_logger(LOGGER_PATH)

# 두 날짜 사이의 년도와 월을 가져오는 함수
def get_years_months_between_dates(past_date):
    current_date = datetime.now()

    # 날짜 리스트 생성
    date_range = pd.date_range(start=past_date, end=current_date, freq='MS')

    # (년, 월) 리스트 생성
    result_list = [(date.year, date.month) for date in date_range]

    return result_list

# 특정 년도와 월의 첫째날과 마지막 날을 가져오는 함수
def get_first_and_last_day(year, month):
    # 첫째날 구하기
    first_day = datetime(year, month, 1)

    # 해당 월의 마지막 날짜 구하기
    last_day = datetime(year, month, monthrange(year, month)[1])

    return first_day, last_day

# 주식 데이터를 CSV 파일로 만드는 함수
def make_stock_csv_file(start, end, folder_path):
    # 데이터를 저장할 빈 DataFrame 생성
    df = pd.DataFrame()

    # 지정된 범위 내의 각 날짜에 대해 루프를 돌면서 데이터를 가져오기
    for date in pd.date_range(start, end):
        date_str = date.strftime("%Y%m%d")
        date_data = stock.get_market_ohlcv(date_str, market="ALL")
        date_fundamental = stock.get_market_fundamental(date_str)
        # 날짜 추가
        date_data["날짜"] = date_str
        # 인덱스(티커) 값 추가
        date_data["종목코드"] = date_data.index.astype(str).tolist()
        # 인덱스(티커) 값을 뽑아내서 종목의 이름으로 변환
        date_data["종목명"] = date_data.index.map(lambda ticker: stock.get_market_ticker_name(ticker))

        # 날짜별 데이터와 기본 데이터를 '종목코드'를 기준으로 병합
        merged_data = pd.merge(date_data, date_fundamental, left_on="종목코드", right_index=True, how="left")

        # '티커' 컬럼을 일반적인 열로 유지하고, 독립적인 순차적인 인덱스를 사용
        df = pd.concat([df, merged_data.reset_index(drop=True)], ignore_index=True)

    # 중복된 데이터 체크 후 중복 제거
    df = df.drop_duplicates()

    stock_file = os.path.join(folder_path, "stock.csv")
    try:
        df.to_csv(stock_file, encoding='utf-8-sig', index=True)  # utf-8-sig는 엑셀에서 한글 깨짐 방지
        logger.info(f'"{stock_file}" 파일이 성공적으로 저장되었습니다.')
    except Exception as e:
        logger.info(f"make_stock_csv_file => df.to_csv() 에러 : {e}")



# 시작 날짜를 입력받아 해당 날짜부터 현재까지의 주식 데이터를 생성하는 함수
def create_stock_files(start_date_str):
    # 시작 날짜 문자열을 datetime 객체로 변환
    start_date = datetime.strptime(start_date_str, "%Y%m%d")

    # 함수를 호출하여 년과 월이 포함된 리스트를 얻습니다.
    result_list = get_years_months_between_dates(start_date)


    for year, month in result_list:
        # 경로 설정
        folder_path = f"{DATA_SAVE_PATH}/{year}/{month:02d}"

        # 주식 데이터가 저장될 파일 경로를 생성합니다.
        stock_path = f"{folder_path}/stock.csv"

        # 설정 경로에 파일 생성
        os.makedirs(folder_path, exist_ok=True)

        # stock.csv 파일이 존재하지 않거나, result_list의 마지막 튜플인 경우
        if not os.path.exists(stock_path) or (year, month) == result_list[-1]:
            # 현재 연도와 월에 해당하는 주식 데이터를 생성하는 함수를 호출하여 파일을 만듭니다.
            first_date, last_date = get_first_and_last_day(year, month)
            make_stock_csv_file(first_date.strftime('%Y%m%d'), last_date.strftime('%Y%m%d'), folder_path)
        else:
            # stock.csv 파일이 이미 존재하는 경우 로그를 출력합니다.
            logger.info(f'"{stock_path}" 파일이 이미 존재합니다.')

