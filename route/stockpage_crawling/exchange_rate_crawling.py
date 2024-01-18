import requests
from bs4 import BeautifulSoup
import json


def exchange_crawling():

    # 환전고시 환율
    url = "https://finance.naver.com/marketindex/exchangeList.naver"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    tbl_exchange = bs_obj.find("table", {"class": "tbl_exchange"})
    tbody = tbl_exchange.find("tbody")

    # 리스트 반환
    tr_list = tbody.find_all("tr")

    # 결과 리스트
    td_list = []
    for tr in tr_list:
        # 각 행(tr)에서 td 태그들을 찾아서 텍스트를 정리하여 리스트에 추가
        td_text_list = [td.text.strip() for td in tr.find_all("td")]

        # 결과 리스트에 추가
        td_list.append(td_text_list)

    # 전달용 딕셔너리
    dic_list = []
    for td in td_list :
        dic = {"name": td[0], "TbRate": td[1], "buy": td[2], "sell": td[3], "send": td[4], "receive": td[5], "exchange": td[6]}
        dic_list.append(dic)

    res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    # print("환율 가격",res)
    return res
