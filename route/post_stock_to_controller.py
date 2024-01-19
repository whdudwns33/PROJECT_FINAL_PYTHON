# 월 단위로 json 데이터를 읽어서 spring boot로 보내는 함수 (file_path)
import requests
import csv
import json
import os
from common.logger_config import config_logger

logger = config_logger('logs/app.log')

def csv_to_json(csv_file_path):
    # CSV 파일 열기
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:
        # CSV 파일을 읽는 csv.reader 객체 생성
        csv_reader = csv.DictReader(csv_file)

        # 첫 번째 행(데이터 인덱스를 나타내는 행)을 제외하고 데이터를 가져오기
        next(csv_reader)

        # 행들을 딕셔너리 리스트로 변환
        data_list = list(csv_reader)

        # 빈 키를 제외하고 새로운 딕셔너리 리스트 생성
        modified_data_list = [{k: v for k, v in row.items() if k != ""} for row in data_list]

        # print(modified_data_list)

        data = json.dumps(modified_data_list, ensure_ascii=False, indent=2)
        return data


def post_json(csv_file_path):
    url = "http://localhost:8111/stock/data"
    data = csv_to_json(csv_file_path)
    logger.info("post_json csv read done")

    try:
        http_post_request = requests.post(url, data=data.encode('utf-8'), headers={'Content-Type': 'application/json'})
        if http_post_request.status_code == 200:
            logger.info("POST 요청 성공")
            print(http_post_request.text)  # 서버에서 보낸 응답 확인
        else:
            logger.error(f"POST 요청 실패. 응답 코드: {http_post_request.status_code}")
            print(http_post_request.text)  # 실패 시 에러 메시지 확인
    except requests.exceptions.ConnectionError as e:
        logger.error(f"ConnectionError: {e}")
