from bs4 import BeautifulSoup
import requests
import json


def rate_crawling():
    # 금리
    url = "https://finance.naver.com/marketindex/"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    table = bs_obj.select_one("#marketindex_aside > div:nth-child(1) > table:nth-child(2)")

    if table is None:
        print("Table not found")
        return

    tbody = table.find("tbody")
    tr_list = tbody.find_all("tr")

    dic_list = []
    for tr in tr_list:
        name = tr.find("th").text.strip()
        interestRate = tr.find_all("td")[0].text
        change_direction = tr.find("img")['alt']
        change_value = tr.find_all("td")[1].text.strip()

        change = change_direction + ' ' + change_value
        dic = {"name": name, "interestRate": interestRate, "change": change}
        dic_list.append(dic)

    print(dic_list)
    res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    return res

rate_crawling()
