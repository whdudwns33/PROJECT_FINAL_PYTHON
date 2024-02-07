from bs4 import BeautifulSoup
import requests
import json


def search_rank_crawling() :
    url = "https://finance.naver.com/sise/lastsearch2.naver"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    div = bs_obj.find("div", {"class": "box_type_l"})
    table = div.find("table", {"class": "type_5"})
    # 헤더 스킵
    trs = table.find_all("tr")[2:]

    stock_data = []

    for tr in trs:
        tds = tr.find_all("td")

        # 각 행의 데이터를 담을 딕셔너리 생성
        stock_entry = {}

        # 행의 각 셀(td)에 대해 반복
        for idx, td in enumerate(tds):
            # 인덱스에 따라 적절한 키로 딕셔너리에 추가
            if idx == 0:
                stock_entry["searchRank"] = td.get_text(strip=True)
            elif idx == 1:
                stock_entry["searchName"] = td.a.get_text(strip=True)
            elif idx == 2:
                stock_entry["searchCount"] = td.get_text(strip=True)
            elif idx == 3:
                stock_entry["searchUpdown"] = td.get_text(strip=True)
            elif idx == 4:
                stock_entry["searchPrice"] = td.get_text(strip=True)
            elif idx == 5:
                stock_entry["searchChangeRate"] = td.get_text(strip=True)
            elif idx == 6:
                stock_entry["searchMarketCap"] = td.get_text(strip=True)

        # 딕셔너리가 비어있지 않을 때만 리스트에 추가
        if stock_entry and any(stock_entry.values()):
            stock_data.append(stock_entry)
    res = json.dumps(stock_data, indent=2, ensure_ascii=False)
    return res

