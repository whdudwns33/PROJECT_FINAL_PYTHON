from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from route.stock_collector import create_stock_files

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['http://localhost:8111'])

scheduler = APScheduler()  # 스케줄러 초기화
scheduler.init_app(app)  # 스케줄러 초기화
scheduler.start()  # 스케줄러 시작

# 1분 간격으로 스케줄 작업 추가
scheduler.add_job(
    func=create_stock_files,
    trigger="cron",
    minute='*/10',
    # hour='*/1',
    id="get_stock_file",
    max_instances=1,
    args=["20231101"]  # 여기에 원하는 날짜 범위를 설정
)

if __name__ == '__main__':
    app.run(debug=True)
