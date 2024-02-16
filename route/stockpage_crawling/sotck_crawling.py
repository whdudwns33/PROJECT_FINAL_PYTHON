import requests
from bs4 import BeautifulSoup
import json



def stock_crawling():
    # 거래 상위
    url = "https://finance.naver.com/"
    response = requests.get(url)
    bs_obj = BeautifulSoup(response.text, "html.parser")
    div_class = bs_obj.find("table", {"class": "tbl_home"})
    top_tbody = div_class.find("tbody", {"id": "_topItems1"})
    # tr 태그를 찾음. 리스트로 저장
    tr_tags = top_tbody.find_all("tr")
    # print(tr_tags)
    # print("-------------------------------------------------------------------------------------------")

    data_list = []
    # 리스트로 저장된 tr을 순회하는 향상된 for문으로 th 정보를 찾음
    for tr in tr_tags:
        th_text = tr.find("th", {"scope": "row"}).text.strip()
        td_price = tr.find("td").text.strip()
        td_ud = tr.em.text.strip()
        # bu_p 의 태그 뒤에 나오는 em이 %를 표시하는 태그이므로 find_next 사용
        td_rate = tr.select_one('td em[class^="bu_p"]').find_next('em').text.strip()

        data_dict = {"name": th_text, "price": td_price, "upDown": td_ud, "rate": td_rate}
        data_list.append(data_dict)

    # print(data_list)
    res = json.dumps(data_list, ensure_ascii=False, indent=4)
    return res

# stock_crawling()
