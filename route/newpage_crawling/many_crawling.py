from bs4 import BeautifulSoup
import requests
import json
import re

def many_crawling():
    url = "https://finance.naver.com/news/news_list.naver?mode=RANK"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    div = bs_obj.find("div", {"class": "hotNewsList _replaceNewsLink"})
    ul = div.find("ul", {"class" : "newsList"})
    lis = ul.find_all("li")

    res = []
    for li in lis:
        href = li.find("a").get("href")
        article_id = re.search('article_id=(\d+)', href)  # href에서 article_id 의 뒤에서 숫자만을 찾아서 저장
        office_id = re.search('office_id=(\d+)', href)  # href에서 office_id 의 뒤에서 숫자만을 찾아서 저장
        link = f"https://n.news.naver.com/mnews/article/{office_id.group(1)}/{article_id.group(1)}"
        # print(link)
        data = {"description": li.text.strip().replace('\n', ''), "link": link }
        res.append(data)

    result = json.dumps(res, ensure_ascii=False, indent=4)
    # print(result)
    return result


