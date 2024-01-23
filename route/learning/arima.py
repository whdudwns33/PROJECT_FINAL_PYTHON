import pandas as pd
from pmdarima import auto_arima
import matplotlib.pyplot as plt
from common.constant import DATA_SAVE_PATH


def get_arima(stock_code, start_date, end_date, future_days=10):
    # CSV 파일 로드
    df = pd.concat([
        pd.read_csv(f"{DATA_SAVE_PATH}/{year}/{month:02d}/stock.csv")
        for year in range(int(start_date[:4]), int(end_date[:4]) + 1)
        for month in range(1, 13)
        if start_date <= f"{year:04d}{month:02d}01" <= end_date
    ])

    # '날짜' 열을 날짜 형식으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')

    # '시가', '고가', '저가', '종가', '거래량', '거래대금', '등락률'이 모두 0인 행 제거
    df = df[(df[['시가', '고가', '저가', '종가', '거래량', '거래대금', '등락률']] != 0).any(axis=1)]

    # '날짜' 열을 날짜 형식으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'], format='%Y%m%d')

    # 선택한 종목 코드에 해당하는 데이터 추출
    selected_stock_data = df[df['종목코드'] == stock_code]

    # '날짜' 열을 인덱스로 설정
    selected_stock_data.set_index('날짜', inplace=True)

    # 종가를 기준으로 한 시계열 데이터 생성
    ts = selected_stock_data['종가']

    # ARIMA 모델 자동으로 찾기
    model = auto_arima(ts, trace=True, suppress_warnings=True, seasonal=False)
    model.fit(ts)

    # 향후 지정된 일 수만큼의 주가 예측
    future_forecast = model.predict(n_periods=future_days)
    future_index = pd.date_range(start=ts.index[-1], periods=future_days + 1, freq='B')[1:]

    # 예측 결과 시각화
    plt.plot(ts, label='Actual Prices')

    # 추가 부분: 향후 예측 결과 그래프에 표시
    plt.plot(future_index, future_forecast, label='Future Prices', linestyle='dashed', color='red')

    plt.title(f'Stock Price Prediction for {stock_code} with ARIMA')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()
