#  app.py
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
from flask_cors import CORS
from route.newpage_crawling.many_crawling import many_crawling
from route.newpage_crawling.real_time_crawling import real_time_crawling
from route.newpage_crawling.tv_crawling import tv_crawling
from route.stockpage_crawling.search_rank import search_rank_crawling
from scheduler.pykrx.stock_collector import create_stock_files
from route.stock_pull.csv_watcher import check_all_csv_files
from route.stockpage_crawling.arg_crawling import arg_crawling
from route.stockpage_crawling.energy_crawling import energy_crawling
from route.stockpage_crawling.gold_crawling import gold_crawling
from route.stockpage_crawling.metal_crawling import metal_crawling
from route.stockpage_crawling.sotck_crawling import stock_crawling
from route.stockpage_crawling.exchange_market_rate_crawling import exchange_market_crawling
from route.stockpage_crawling.exchange_rate_crawling import exchange_crawling
from route.stockpage_crawling.oil_price_crawling import oil_crawling
from route.mainpage_crawling.overseas_indicators_crawling import overseas_indicators_crawling
from route.mainpage_crawling.domestic_indicators_crawling import domestic_indicators_crawling
from route.mainpage_crawling.majornews_crawling import majornews_crawling
from route.mainpage_crawling.rate_crawling import rate_crawling
from route.learning.arima import get_arima
from scheduler.news.news import get_news
from common.constant import SPRING_BOOT_DOMAIN
import os


class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=[f"{SPRING_BOOT_DOMAIN}"])

# 파이썬 크롤링
app.add_url_rule('/python/stock', '/python/stock', stock_crawling, methods=['GET'])
app.add_url_rule('/python/exchange', '/python/exchange', exchange_crawling, methods=['GET'])
app.add_url_rule('/python/exchangeMarket', '/python/exchangeMarket', exchange_market_crawling, methods=['GET'])
app.add_url_rule('/python/energy', '/python/energy', energy_crawling, methods=['GET'])
app.add_url_rule('/python/arg', '/python/arg', arg_crawling, methods=['GET'])
app.add_url_rule('/python/gold', '/python/gold', gold_crawling, methods=['GET'])
app.add_url_rule('/python/metal', '/python/metal', metal_crawling, methods=['GET'])
app.add_url_rule('/python/oil', '/python/oil', oil_crawling, methods=['GET'])
app.add_url_rule('/python/search', '/python/search', search_rank_crawling, methods=['GET'])
app.add_url_rule('/python/overseasIndicators', '/python/overseasIndicators', overseas_indicators_crawling, methods=['GET'])
app.add_url_rule('/python/domesticIndicators', '/python/domesticIndicators', domestic_indicators_crawling, methods=['GET'])
app.add_url_rule('/python/majornews', '/python/majornews', majornews_crawling, methods=['GET'])
app.add_url_rule('/python/manynews', '/python/manynews', many_crawling, methods=['GET'])
app.add_url_rule('/python/tvnews', '/python/tvnews', tv_crawling, methods=['GET'])
app.add_url_rule('/python/rtnews', '/python/rtnews', real_time_crawling, methods=['GET'])

app.add_url_rule('/python/rate', '/python/rate', rate_crawling, methods=['GET'])
app.add_url_rule('/python/stock/pull', '/python/stock/pull', check_all_csv_files, methods=['GET'])


# Spring Boot에서 Arima 데이터 POST요청
@app.route('/python/arima', methods=['POST'])
def arima_route():
    data = request.get_json()
    stock_code = data.get('stock_code')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    column_type = data.get('column_type')
    future_days = int(data.get('future_days', 0))

    print(stock_code, start_date, end_date, column_type, future_days)

    result = get_arima(stock_code, start_date, end_date, column_type, future_days)

    return jsonify(result)


scheduler = APScheduler()  # 스케줄러 초기화
scheduler.init_app(app)  # 스케줄러 초기화

# 10분 간격으로 pykrx api 주식 데이터 수집
scheduler.add_job(
    func=create_stock_files,
    trigger="cron",
    minute='*/1',
    # hour='*/1',
    id="get_stock_files",
    max_instances=1,
    args=["20230101"]  # 여기에 원하는 날짜 범위를 설정
)

scheduler.add_job(
    func=get_news,
    # trigger="cron",
    # hour='*/24',
    trigger=IntervalTrigger(minutes=30),
    id="get_news",
    max_instances=1,
    args=[]
)

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.start()
    app.run(debug=True)


