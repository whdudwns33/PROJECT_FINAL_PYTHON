from bs4 import BeautifulSoup
import requests
import json

headers = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}

def hotranking_crawling():
    # 핫랭킹
    url = "https://m.stock.naver.com/"
    response = requests.get(url, headers=headers)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    table = bs_obj.find("div", {"class": "LayoutCard_article__27nL4 type_space"})
    li_list = table.select_one("ul > li:nth-child(1) > div:nth-child(1)")

    # dic_list = []
    # for li in li_list:
    #     rank = li.find("em", {"class": "TableList_count__njjJB"}).text
    #     name = li.find("div", {"class": "TableList_name__5Num5"}).text
    #     price = li.find("div", {"class": "TableList_price__Vibzp"}).text
    #     market_cap = li.find_all("span", {"class": "TableList_market__2lMjv"})[0].text
    #     volume = li.find_all("span", {"class": "TableList_market__2lMjv"})[1].text
    #     total = li.find("span", {"class": "TableList_total__Wl25W"}).text
    #     link = li.find("a", {"class": "TableList_link__UONz9"})['href']
    #
    #     dic = {"rank": rank, "name": name, "price": price, "market_cap": market_cap, "volume": volume, "total": total,
    #            "link": link}
    #     dic_list.append(dic)
    #
    # res = json.dumps(dic_list, ensure_ascii=False, indent=4)
    print(li_list)
    # return res

hotranking_crawling()
