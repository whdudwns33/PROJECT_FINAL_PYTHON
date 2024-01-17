from bs4 import BeautifulSoup
import requests
import json

# 에너지
url = "https://finance.naver.com/marketindex/?tabSel=gold#tab_section"
response = requests.get(url)
bs_obj = BeautifulSoup(response.text, "html.parser")
table = bs_obj.find("table", {"summary": "귀금속 리스트"})
tbody = table.find("tbody")
tr_list = tbody.find_all("tr")

td_list = []
for tr in tr_list :
    text = [td.text.split() for td in tr.find_all("td")]
    td_list.append(text)


# 수정 필요
dic_list = []
for td in td_list:
    dic = {"name" : td[0][0] , "unit": td[1][0] + td[1][1], "price": td[2], "yesterday": td[3], "rate": td[4], "date": td[5]}
    print(dic)