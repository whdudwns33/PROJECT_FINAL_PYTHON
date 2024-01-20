import datetime
import json
import os
import urllib.request
import csv
from glob import glob
import requests
def collect_news_to_csv():
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
            # print(items)
            # os.makedirs('news_data', exist_ok=True)

            for item in items:
                if 'pubDate' in item and item['pubDate']:
                    # pubDate에서 year와 month 추출
                    pub_date = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
                    year = pub_date.strftime('%Y')
                    month = pub_date.strftime('%m')
                    year_month_day = pub_date.strftime('%Y%m%d')
                    item['pubDate'] = year_month_day

                    # 연도와 월에 해당하는 디렉토리 생성
                    news_dir = f"../news_data/{year}/{month}"
                    os.makedirs(news_dir, exist_ok=True)

                    # csv 파일 생성 및 작성
                    news_path = os.path.join(news_dir, f"{month}_news.csv")
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
    collect_news_to_csv()
    
    url = "http://localhost:8111/news/save"
    all_news = []
    file_names = glob("../news_data/*/*/*.csv")
    for file_name in file_names:
        news_list = read_csv_to_dict_list(file_name)
        all_news.extend(news_list)

    response = requests.post(url, json=all_news)
    if response.status_code == 200:
        print("news sent successfully!")
    else:
        print(f"Failed to send news. Status code: {response.status_code}")
        print(response.text)




