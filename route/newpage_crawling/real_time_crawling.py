from bs4 import BeautifulSoup
import requests
import json
import re

def real_time_crawling():
    url = "https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    ul = bs_obj.find("ul", {"class": "realtimeNewsList _replaceNewsLink"})
    li = ul.find("li", {"class":"newsList top"})
    di = li.find("dl")
    dds = di.find_all("dd")

    res = []
    for dd in dds:
        dda = li.find("a")
        if dda:
            text = dd.text.strip().replace('\n', '').strip().replace('\t', '')
            href = dda.get("href")
            article_id = re.search('article_id=(\d+)', href)  # href에서 article_id 의 뒤에서 숫자만을 찾아서 저장
            office_id = re.search('office_id=(\d+)', href)  # href에서 office_id 의 뒤에서 숫자만을 찾아서 저장
            link = f"https://n.news.naver.com/mnews/article/{office_id.group(1)}/{article_id.group(1)}"
            # print(link)
            data = {"description": text, "link": link}
            res.append(data)
    result = json.dumps(res, ensure_ascii=False, indent=4)
    # print(result)
    return result
