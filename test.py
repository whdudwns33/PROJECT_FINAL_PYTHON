from route.learning.lstm import lstm_predict
#
from route.learning.arima import get_arima

stock_code = "005930"  # Replace with your desired stock code
start_date = "20240101"  # Replace with your desired start date
end_date = "20240201"  # Replace with your desired end date
column_type = "종가"  # Replace with the column type you want to predict (e.g., 종가, 시가, 고가, 저가)


lstm_predict(stock_code, start_date, end_date, column_type)
# get_arima(stock_code, start_date, end_date, column_type, 10)
# # print(get_arima(stock_code, start_date, end_date, column_type, 10))