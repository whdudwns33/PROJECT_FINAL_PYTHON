import re
from bs4 import BeautifulSoup
import requests
import json

def tv_crawling():
    url = "https://finance.naver.com/news/news_list.naver?mode=TV&section_id=tv"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    div = bs_obj.find("div", {"class": "photoNewsList _replaceNewsLink"})
    ul = div.find("ul", {"class" : "newsList"})
    lis = ul.find_all("li")

    res = []
    for li in lis:
        thumb = li.find("img").get("src")
        text = li.text.strip().replace('\n', '')
        href = li.find("a").get("href")
        article_id = re.search('article_id=(\d+)', href)  # href에서 article_id 의 뒤에서 숫자만을 찾아서 저장
        office_id = re.search('office_id=(\d+)', href)  # href에서 office_id 의 뒤에서 숫자만을 찾아서 저장
        link = f"https://n.news.naver.com/mnews/article/{office_id.group(1)}/{article_id.group(1)}"
        # print(link)
        data = {"description": text.strip().replace('\t', '') , "link": link, "thumb" : thumb}
        res.append(data)

    result = json.dumps(res, ensure_ascii=False, indent=4)
    return result
