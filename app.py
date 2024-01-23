from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from route.pykrx_api.stock_collector import create_stock_files
from route.pykrx_api.csv_watcher import check_all_csv_files

from route.stockpage_crawling.arg_crawling import arg_crawling
from route.stockpage_crawling.energy_crawling import energy_crawling
from route.stockpage_crawling.gold_crawling import gold_crawling
from route.stockpage_crawling.metal_crawling import metal_crawling
from route.stockpage_crawling.sotck_crawling import stock_crawling
from route.stockpage_crawling.exchange_market_rate_crawling import exchange_market_crawling
from route.stockpage_crawling.exchange_rate_crawling import exchange_crawling
from route.stockpage_crawling.oil_price_crawling import oil_crawling
from route.news import get_news
import os


class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=['http://localhost:8111'])

# 파이썬 크롤링
app.add_url_rule('/python/stock', '/python/stock', stock_crawling, methods=['GET'])
app.add_url_rule('/python/exchange', '/python/exchange', exchange_crawling, methods=['GET'])
app.add_url_rule('/python/exchangeMarket', '/python/exchangeMarket', exchange_market_crawling, methods=['GET'])
app.add_url_rule('/python/energy', '/python/energy', energy_crawling, methods=['GET'])
app.add_url_rule('/python/arg', '/python/arg', arg_crawling, methods=['GET'])
app.add_url_rule('/python/gold', '/python/gold', gold_crawling, methods=['GET'])
app.add_url_rule('/python/metal', '/python/metal', metal_crawling, methods=['GET'])
app.add_url_rule('/python/oil', '/python/oil', oil_crawling, methods=['GET'])
# # 임시 뉴스
# app.add_url_rule('/python/elastic/news', '/python/elastic/news', get_news, methods=['GET'])



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
    args=["20230101"]  # 여기에 원하는 날짜 범위를 설정
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

# 24시간 간격으로 엘라스틱에 데이터 저장
scheduler.add_job(
    func=get_news,
    trigger="cron",
    minute='*/1',
    # hour='*/24',
    id="get_news",
    max_instances=1,
    args=[]
)




if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.start()
    app.run(debug=True)