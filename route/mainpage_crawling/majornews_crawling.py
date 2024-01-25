from bs4 import BeautifulSoup
import requests
import re
import json
import time


def majornews_crawling():
    # 주요뉴스
    url = "https://finance.naver.com/news/mainnews.naver"
    response = requests.get(url)

    # 페이지 로딩을 기다립니다.
    # time.sleep(1)  # 5초 동안 대기

    bs_obj = BeautifulSoup(response.text, "html.parser")
    news_list = bs_obj.find("div", {"class": "mainNewsList _replaceNewsLink"} ).find_all("li", {"class": "block1"})

    news_data = []
    for news in news_list:
        a_tag = news.find("dd", {"class": "articleSubject"}).find("a")
        href = a_tag.get('href')
        article_id = re.search('article_id=(\d+)', href) # href에서 article_id 의 뒤에서 숫자만을 찾아서 저장
        office_id = re.search('office_id=(\d+)', href) # href에서 office_id 의 뒤에서 숫자만을 찾아서 저장
        if article_id and office_id:
            name = a_tag.text
            link = f"https://n.news.naver.com/mnews/article/{office_id.group(1)}/{article_id.group(1)}"
            summary = news.find("dd", {"class": "articleSummary"}).text.strip().split('\n')[0]
            media = news.find("span", {"class": "press"}).text
            date = news.find("span", {"class": "wdate"}).text
            news_data.append({'name': name, 'link': link, 'summary': summary, 'media': media, 'date': date})

    # print(news_list)
    return news_data

# majornews_crawling()
# print(majornews_crawling())