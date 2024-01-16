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
    res = [td.text.split() for td in tr.find_all("td")]
    td_list.append(res)

dic_list = []
for text in td_list :
    dic = {"name": text[0][0], "unit": text[1][0]+text[1][1]+text[1][2], "price": text[2][0], "yesterday": text[3][0], "rate": text[4][0], "date": text[5][0]}
    dic_list.append(dic)
print(dic_list)
