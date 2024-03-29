import pandas as pd
from pmdarima import auto_arima
import matplotlib.pyplot as plt
from common.constant import DATA_SAVE_PATH, LOGGER_PATH
from common.logger_config import config_logger

# 로거 설정
# 'logs/app.log' 파일에 로그를 기록하는 로거를 설정
logger = config_logger(LOGGER_PATH)

def load_stock_data(start_date, end_date):
    df = pd.concat(
        [
            pd.read_csv(f"{DATA_SAVE_PATH}/{year}/{month:02d}/stock.csv")
            for year in range(int(start_date[:4]), int(end_date[:4]) + 1)
            for month in range(1, 13)
            if start_date <= f"{year:04d}{month:02d}" <= end_date
        ]
    )

    # '날짜' 열을 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")

    # '시가', '고가', '저가', '종가', '거래량', '거래대금', '등락률'이 모두 0인 행 제거
    df = df[
        (df[["시가", "고가", "저가", "종가", "거래량", "거래대금", "등락률"]] != 0).any(
            axis=1
        )
    ]

    # '날짜' 열을 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")

    return df


def get_arima(stock_code, start_date, end_date, column_type, future_days=10):
    # df에서 계산에 필요한 데이터만 추출
    df = load_stock_data(start_date, end_date)

    # 선택한 종목 코드에 해당하는 데이터 추출
    selected_stock_data = df[df["종목코드"] == stock_code]

    # '날짜' 열을 인덱스로 설정
    selected_stock_data.set_index("날짜", inplace=True)

    # 종가를 기준으로 한 시계열 데이터 생성
    ts = selected_stock_data[column_type]

    if future_days > 0:
        # ARIMA 모델 자동으로 찾기
        model = auto_arima(ts, trace=True, suppress_warnings=True, seasonal=False)
        model.fit(ts)

        # 향후 지정된 일 수만큼의 주가 예측
        future_forecast = model.predict(n_periods=future_days)
        future_forecast_rounded = [int(round(val, 1)) for val in future_forecast]  # 반올림

        future_index = pd.date_range(start=ts.index[-1], periods=future_days + 1, freq="B")[
            1:
        ]
        result = {
            "stock_code": stock_code,
            "column_type": column_type,
            'actual_price': {'data': ts.tolist(), 'index': ts.index.strftime('%Y-%m-%d').tolist()},
            'future_price': {'data': future_forecast_rounded, 'index': future_index.strftime('%Y-%m-%d').tolist()},
        }
    else:
        result = {
            "stock_code": stock_code,
            "column_type": column_type,
            'actual_price': {'data': ts.tolist(), 'index': ts.index.strftime('%Y-%m-%d').tolist()},
            'future_price': {'data': [], 'index': []},
        }

    # # 예측 결과 시각화
    # plt.plot(ts, label="Actual Prices")
    #
    # # 추가 부분: 향후 예측 결과 그래프에 표시
    # plt.plot(
    #     future_index,
    #     future_forecast,
    #     label="Future Prices",
    #     linestyle="solid",
    #     color="red",
    # )
    #
    # plt.title(f"Stock Price Prediction for {stock_code} with ARIMA")
    # plt.xlabel("Date")
    # plt.ylabel("Stock Price")
    # plt.legend()
    # plt.show()

    logger.info(f"Arima Chart 요청이 확인되었습니다! 스프링 부트에 JSON 데이터를 보냅니다... "
                f"( 종목코드: '{stock_code}', "
                f"데이터 타입: '{column_type}', "
                f"시작일: '{start_date}', "
                f"종료일: '{end_date}', "
                f"예측일수: {future_days} )")

    return result