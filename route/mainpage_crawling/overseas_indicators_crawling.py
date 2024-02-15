from bs4 import BeautifulSoup
import requests
import json


def overseas_indicators_crawling():
    # 해외시장지표
    url = "https://finance.naver.com/"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    table = bs_obj.find("div", {"class": "aside_area aside_stock"})
    tbody = table.find("tbody")
    tr_list = tbody.find_all("tr")

    dic_list = []
    for tr in tr_list:
        name = tr.find("th").text.strip()
        price = tr.find_all("td")[0].text
        change = tr.find_all("td")[1].text

        dic = {"name": name, "price": price, "change": change}
        dic_list.append(dic)

    print(dic_list)
    res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    return res


overseas_indicators_crawling()