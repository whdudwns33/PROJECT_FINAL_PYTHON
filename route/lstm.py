import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
from glob import glob

# 삼성 주식 예제: '005930'
ticker = input()

# 함수식으로 선언할 때, 아래 함수 활성화
# def lstm_predict(ticker) :
# 폴더 내의 모든 csv파일 목록을 불러온다

file_names = glob("../data/*/*/stock.csv")
# print(file_names)

# df_all을 데이터프레임으로 초기화
df_all = pd.DataFrame()

for file_name in file_names:
    df = pd.read_csv(file_name, encoding='utf-8')
    input_df = df[(df['종목코드'] == ticker) & (df['종가'] != 0)]
    df_all = pd.concat([df_all, input_df], ignore_index=True)

# 종가 기준 파싱
# reshape(-1, 1)는 열 데이터를 행 데이터로 변환
data = df_all['종가'].values.reshape(-1, 1)
# print("data",data)

# 데이터의 총 수 - 1 : 현제 기(term)에서 몇 전기 까지 볼껀지
# 0.88가 가장 적절한 수준인듯
length = int(len(data) * 0.88)
# length = 180
# print("length",length)


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
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dense(units=25))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델 학습
model.fit(x_train, y_train, batch_size=1, epochs=1)

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
print("Future Predictions:", future_predictions[0:5])



# # Plot the results
# # 학습용 80%
# train = df_all[:train_size]
# # 검증용 20%
# valid = df_all[train_size:]
# valid['Predictions'] = predictions
# # print("",valid['Predictions'])
#
# plt.figure(figsize=(100, 8))
# plt.title('Stock Price Prediction using LSTM')
# plt.xlabel('Date')
# plt.ylabel('Closing Price (KRW)')
# plt.xticks(np.arange(0, len(valid['날짜']), step=10), rotation=45)
# plt.plot(train['날짜'], train['종가'], label='Train')
# # 검증 데이터 Validation, 사용되지 않은 20%
# plt.plot(valid['날짜'], valid['종가'], label='Validation')
# # 예측 데이터 Predictions
# plt.plot(valid['날짜'], valid['Predictions'], label='Predictions')
# plt.legend(loc='lower right')
# plt.show()
# # 사용되지 않은 20%와 예측 데이터를 비교하는 그래프