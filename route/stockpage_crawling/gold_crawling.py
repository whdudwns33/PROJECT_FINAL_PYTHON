from bs4 import BeautifulSoup
import requests
import json


def gold_crawling():
    # 금
    url = "https://finance.naver.com/marketindex/?tabSel=gold#tab_section"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    table = bs_obj.find("table", {"summary": "귀금속 리스트"})
    tbody = table.find("tbody")
    tr_list = tbody.find_all("tr")

    td_list = []
    for tr in tr_list :
        text = [td.text.strip() for td in tr.find_all("td")]
        td_list.append(text)

    dic_list = []
    for data in td_list:
        dic = {"name": data[0], "unit": data[1], "price": data[2], "yesterday": data[3], "rate": data[4], "date": data[5]}
        dic_list.append(dic)

    res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    return res
# print(dic_list)