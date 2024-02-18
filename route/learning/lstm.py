from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from glob import glob
# csv 파일 읽어오는 Path
from common.constant import DATA_SAVE_PATH


# # 삼성 주식 예제: '005930'
# ticker = input()

# 함수식으로 선언할 때, 아래 함수 활성화
def lstm_predict(stock_code, start_date, end_date, column_type) :
# 폴더 내의 모든 csv파일 목록을 불러온다
    file_names = glob(f"{DATA_SAVE_PATH}/*/*/stock.csv")
    # print("file_names",file_names)

    # df_all을 데이터프레임으로 초기화
    df_all = pd.DataFrame()

    for file_name in file_names:
        df = pd.read_csv(file_name, encoding='utf-8')
        input_df = df[(df['종목코드'] == stock_code) & (df[column_type] != 0)]
        df_all = pd.concat([df_all, input_df], ignore_index=True)

    # 종가 기준 파싱
    # reshape(-1, 1)는 열 데이터를 행 데이터로 변환
    # print(df_all)
    data = df_all['종가'].values.reshape(-1, 1)
    # print("data",data)

    # 데이터의 총 수 - 1 : 현제 기(term)에서 몇 전기 까지 볼껀지
    length = int(len(data) * 0.92)
    print("length",length)
    print("Number of rows in df_all:", len(df_all))


    # 데이터 정규화
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    # print("scaled_data",scaled_data)

    # 학습 데이터 생성
    # 전체 데이터셋 중 80%를 훈련에 사용하고, 나머지 20%를 검증에 사용
    # train_size = int(len(scaled_data) * 0.8)

    # 전체 데이터 학습
    train_size = int(len(scaled_data)-1)
    # :train_size-> 처음 부터 train_size 정도 만큼과 나머지를 슬라이싱
    train_data = scaled_data[:train_size, :]
    x_train, y_train = [], []
    # print("x_train", x_train)
    # print("y_train", y_train)


    for i in range(length, len(train_data)):
        x_train.append(train_data[i-length:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # LSTM 모델 생성
    # Sequential() : 선형 모델 선언
    # LSTM, Dense 레이어는 너무 많으면 과적합 문제가 발생
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    # 평균 제곱 오차(MSE로 SSR과 비슷하지만 다른 개념) : 0에 가까울 수록 설명력이 높음. R^2랑 다른 것.
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습
    # epoch는 모델이 훈련 데이터를 한 번씩 학습하는 주기를 의미합니다.
    # batch_size는 한 번의 모델 업데이트에 사용되는 데이터 샘플의 수를 나타냅니다.
    model.fit(x_train, y_train, batch_size=1, epochs=8)

    # 데이터 셋 생성
    test_data = scaled_data[train_size - length:, :]
    x_test = []

    for i in range(length, len(test_data)):
        x_test.append(test_data[i-length:i, 0])

    # x_test를 만드는 과정은 LSTM 모델에 예측을 수행하기 위한 입력 데이터를 생성하는 것
    x_test = np.array(x_test)
    # print("x_test", x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    # print("x_test", x_test)

    # 예측 값(검증)
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    print("Predictions:", predictions[0:5])


    # 미래 데이터 예측
    future_length = 5
    future_data = scaled_data[future_length:, :]
    x_future = []

    for i in range(length, len(future_data)):
        x_future.append(future_data[i-length:i, 0])

    x_future = np.array(x_future)
    x_future = np.reshape(x_future, (x_future.shape[0], x_future.shape[1], 1))

    # 미래 예측
    future_predictions = model.predict(x_future)
    future_predictions = scaler.inverse_transform(future_predictions)


    # 미래 예측값 출력
    future_predictions_list = future_predictions.flatten().tolist()


# 날짜 인덱스 생성
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
    # 선택한 종목 코드에 해당하는 데이터 추출
    selected_stock_data = df[df["종목코드"] == stock_code]
    # '날짜' 열을 인덱스로 설정
    selected_stock_data.set_index("날짜", inplace=True)

    # 미래 날짜 인덱스 생성
    start_date = datetime.today() + timedelta(days=1)
    end_date = start_date + timedelta(days=10)
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]


    # 종가를 기준으로 한 시계열 데이터 생성
    ts = selected_stock_data[column_type]


    if len(future_predictions_list) > 0:
        result = {
            "stock_code": stock_code,
            "column_type": column_type,
            'actual_price': {'data': ts.tolist(), 'index': ts.index.strftime('%Y-%m-%d').tolist()},
            'future_price': {'data': future_predictions_list[0:10],
                             'index': [date.strftime('%Y-%m-%d') for date in date_range]},
        }
    else:
        result = {
            "stock_code": stock_code,
            "column_type": column_type,
            'actual_price': {'data': ts.tolist(), 'index': ts.index.strftime('%Y-%m-%d').tolist()},
            'future_price': {'data': [], 'index': []},
        }

    print("결과 : ",result)
    return result