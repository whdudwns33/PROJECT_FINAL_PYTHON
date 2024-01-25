from bs4 import BeautifulSoup
import requests
import json


def domestic_indicators_crawling():
    # 국내시장지표
    url = "https://finance.naver.com/sise/"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    div = bs_obj.find("div", {"class": "lft"})
    ul = div.select_one("#contentarea > div.box_top_submain2 > div.lft > ul")
    li_list = ul.find_all("li")

    dic_list = []
    for li in li_list:
        a_tag = li.find("a")
        spans = a_tag.find_all("span")
        name = spans[0].text
        price = spans[1].text
        change = spans[2]
        change_info = spans[2].text.strip('\n').replace('상승', '')
        # changepoint = change_info.find("span", {"class": ["nup", "ndown"]}).text
        # changestatus = change.find("span", {"class": "blind"}).text

        dic = {"name": name, "price": price, "changepoint": change_info}
        dic_list.append(dic)


    res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    # print(res)
    return res


domestic_indicators_crawling()
