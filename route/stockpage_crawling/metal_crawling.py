from bs4 import BeautifulSoup
import requests
import json



def metal_crawling():
    # 철강
    url = "https://finance.naver.com/marketindex/?tabSel=materials#tab_section"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    table = bs_obj.find("table", {"summary": "비철금속"})
    tbody = table.find("tbody")
    tr_list = tbody.find_all("tr")

    td_list = []
    for tr in tr_list:
        text = [td.text.replace('\n', '').replace('\t', '').strip() for td in tr.find_all("td")]
        td_list.append(text)

    dic_list = []
    for res in td_list:
        dic = {"name": res[0],  "units": res[1], "price": res[2], "yesterday": res[3], "rate": res[4], "date": res[5], "": res[6]}
        dic_list.append(dic)

    res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    return res
# print(dic_list)