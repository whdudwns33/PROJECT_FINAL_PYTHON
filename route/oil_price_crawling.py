import requests
from bs4 import BeautifulSoup
import json


# 국제 유가
url = "https://finance.naver.com/marketindex/?tabSel=gold#tab_section"

response = requests.get(url)
bs_obj = BeautifulSoup(response.text, "html.parser")
table = bs_obj.find("table", {"class": "tbl_exchange"})
tbody = table.find("tbody")

tr_list = tbody.find_all("tr")

td_list = []
for tr in tr_list:
    res = [tr.find_all("td")]
    td_list.append(res)
print(td_list)
