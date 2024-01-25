import datetime
import json
import os
import urllib.request
import csv
from glob import glob
import requests
from common.constant import SPRING_BOOT_DOMAIN

def collect_news_to_csv():
    print("뉴스 수집 실행")
    client_id = "73M8oVppQg4z20jwcfdY"
    client_secret = "dY8gYRoFso"
    queries = ['주식', '경제', '문화', '정치', '사회', '외교']
    for query in queries:
        encText = urllib.parse.quote(query)
        url = "https://openapi.naver.com/v1/search/news?query=" + encText + "&display=100"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read().decode("utf-8")
            response_data = json.loads(response_body)
            items = response_data.get('items', [])

            for index, item in enumerate(items):
                if 'pubDate' in item and item['pubDate']:
                    # pubDate에서 year, month, day 추출
                    pub_date = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
                    year = pub_date.strftime('%Y')
                    month = pub_date.strftime('%m')
                    day = pub_date.strftime('%d')
                    year_month_day = pub_date.strftime('%Y%m%d')
                    item['pubDate'] = year_month_day

                    # ID 값 추가 (날짜 + 인덱스 값)
                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime('%Y%m%d%H%M%S')
                    item['id'] = f"{formatted_datetime}_{queries.index(query)}_{index}"

                    # 연도와 월에 해당하는 디렉토리 생성
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    news_data_dir = os.path.join(script_dir, '../news_data', year, month, day)
                    # 해당 경로에 파일이 존재하면 파일을 만들지 않음
                    os.makedirs(news_data_dir, exist_ok=True)

                    # csv 파일 생성 및 작성
                    news_path = os.path.join(news_data_dir, f"news_data.csv")
                    with open(news_path, 'a', newline='', encoding='utf-8') as csvfile:
                        fieldnames = item.keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                        # 파일이 비어 있는 경우 헤더 작성
                        if os.path.getsize(news_path) == 0:
                            writer.writeheader()

                        writer.writerow(item)

        else:
            print("Error Code:" + rescode)

# csv 파일을 읽는 함수
def read_csv_to_dict_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def get_news():
    print("뉴스 엘라스틱 실행")
    # 데이터 수집
    try:
        collect_news_to_csv()

        url = f"{SPRING_BOOT_DOMAIN}/news/save"
        all_news = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        news_data_dir = os.path.join(script_dir, '../news_data')
        file_names = glob(os.path.join(news_data_dir, '*/*/*.csv'))

        for file_name in file_names:
            news_list = read_csv_to_dict_list(file_name)
            all_news.extend(news_list)

        response = requests.post(url, json=all_news)
        if response.status_code == 200:
            print("news sent successfully!")
        else:
            print(f"Failed to send news. Status code: {response.status_code}")
            print(response.text)

    except Exception as e:
            print(e)