from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from route.stock_collector import create_stock_files
from route.csv_watcher import check_all_csv_files
import os

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['http://localhost:8111'])

scheduler = APScheduler()  # 스케줄러 초기화
scheduler.init_app(app)  # 스케줄러 초기화


# 10분 간격으로 pykrx api 주식 데이터 수집
scheduler.add_job(
    func=create_stock_files,
    trigger="cron",
    minute='*/10',
    # hour='*/1',
    id="get_stock_files",
    max_instances=1,
    args=["20231101"]  # 여기에 원하는 날짜 범위를 설정
)

# 1분 간격으로 csv파일 내용 변경 체크
scheduler.add_job(
    func=check_all_csv_files,
    trigger="cron",
    minute='*/1',
    id="check_stock_files",
    max_instances=1,
    args=["data/", "hashes/"]  # 다른 작업에 필요한 매개변수 전달
)

@app.route('/')
def home():
    return "Welcome to the Flask API!"

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.start()
    app.run(debug=True)