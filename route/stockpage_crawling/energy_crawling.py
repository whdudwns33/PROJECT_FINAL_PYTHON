from bs4 import BeautifulSoup
import requests
import json

def energy_crawling():
    # 에너지
    url = "https://finance.naver.com/marketindex/?tabSel=materials#tab_section"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    table = bs_obj.find("table", {"summary": "에너지 선물"})
    tbody = table.find("tbody")
    tr_list = tbody.find_all("tr")

    td_list = []
    for tr in tr_list:
        text = [td.text.replace('\n', '').replace('\t', '').strip() for td in tr.find_all("td")]
        td_list.append(text)

    dic_list = []
    for res in td_list:
        # , "yesterday": res[4]
        dic = {"name": res[0], "month": res[1], "units": res[2], "price": res[3], "rate": res[5], "date": res[6], "exchange": res[7]}
        dic_list.append(dic)

    res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    return res
# print(dic_list)