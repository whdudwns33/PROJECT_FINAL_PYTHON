from flask import Flask, request, jsonify
from route.learning.lstm import lstm_predict

app = Flask(__name__)

@app.route('/python/lstm', methods=['POST'])
def lstm_route():
    data = request.get_json()
    stock_code = data.get('stock_code')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    column_type = data.get('column_type')

    # 여기에서 lstm_predict 함수를 직접 호출
    result_value = lstm_predict(stock_code, start_date, end_date, column_type)

    try:
        return jsonify(result_value)
    except Exception as e:
        print("Error:", str(e))
        return jsonify(result_value)

if __name__ == '__main__':
    app.run(port=5001)
