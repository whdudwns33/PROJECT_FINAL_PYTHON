from common.logger_config import config_logger
import hashlib
import os
from route.pykrx_api.post_stock_to_controller import post_json
from common.constant import LOGGER_PATH, DATA_SAVE_PATH, HASH_SAVE_PATH, PROCESS_NUMBER
from flask import jsonify
from datetime import datetime, timedelta

# 로거 설정
# 'logs/app.log' 파일에 로그를 기록하는 로거를 설정
logger = config_logger(LOGGER_PATH)


# 주어진 파일의 해시값(MD5)을 계산하여 반환하는 함수
def get_file_hash(file_path):
    # open 함수를 사용하여 파일을 열고, 그 파일을 이진 모드('rb': read binary)로 열어서 파일의 내용을 읽어오고 있음
    with open(file_path, 'rb') as file:
        file_content = file.read()
        return hashlib.md5(file_content).hexdigest()


# 주어진 파일의 해시값이 마지막으로 저장된 해시값과 다른지 확인하는 함수입니다.
def is_file_changed(file_path, last_hash):
    current_hash = get_file_hash(file_path)
    return current_hash != last_hash


# 주어진 파일에 저장된 마지막 해시파일을 읽어오는 함수입니다.
def get_last_hash_from_file(file_path):
    try:
        with open(file_path, 'r') as hash_file:
            return hash_file.read().strip()
    except FileNotFoundError:
        return None


# 주어진 파일에 새로운 해시값을 저장하는 함수입니다.
def save_hash_to_file(file_path, hash_value):
    # 파일이 위치할 디렉토리를 만듭니다. 이미 디렉토리가 존재하면 에러를 발생시키지 않습니다.
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 주어진 파일에 새로운 해시값을 쓰기 모드로 저장합니다.
    with open(file_path, 'w') as hash_file:
        hash_file.write(hash_value)

def get_year_month_from_file(file_path):
    # 파일 경로에서 년과 월을 추출합니다.
    # 예: "/some/path/2022/01/stock.csv"에서 "202201"을 추출
    _, year, month, _ = file_path.split(os.path.sep)
    return f"{year}{month}"


# 주어진 디렉토리 내의 모든 CSV 파일에 대해 해시값을 체크하는 함수입니다.

def check_all_csv_files():
    try:
        files_processed = 0
        num_files_to_process = PROCESS_NUMBER

        # # 현재 날짜와 이전 달 계산
        # current_date = datetime.now()
        # last_month = current_date - timedelta(days=current_date.day + 1)
        #
        # # 현재 년월 및 이전 달 년월 계산
        # current_year_month = current_date.strftime("%Y%m")
        # last_month_year_month = last_month.strftime("%Y%m")

        # 현재 년월 계산
        current_year_month = datetime.now().strftime("%Y%m")

        # 주어진 디렉토리 내의 모든 파일을 확인
        for root, _, files in os.walk(DATA_SAVE_PATH):
            for file_name in files:
                # 파일 확장자가 .csv 인지 확인
                if file_name.lower().endswith(".csv"):
                    file_path = os.path.join(root, file_name)

                    # 현재 csv 파일의 해시값을 계산
                    current_hash = get_file_hash(file_path)
                    # 해시 파일의 경로 구성
                    hash_relative_path = os.path.relpath(file_path, DATA_SAVE_PATH)
                    hash_file_path = os.path.join(HASH_SAVE_PATH, f"{hash_relative_path}.hash")

                    # 저장된 마지막 해시 파일의  해시 값 가져오기
                    last_hash = get_last_hash_from_file(hash_file_path)

                    # 저장된 해시값이 없거나 저장된 해시파일의 경로가 현재 년 월 이고 양쪽의 해시 값이 다르면 실행
                    if last_hash is None or(get_year_month_from_file(hash_file_path) == current_year_month and current_hash != last_hash):

                        # csv 파일 경로에서 year_month 추출
                        year_month = get_year_month_from_file(file_path)

                        logger.info(f"hash값이 변경되었습니다! 스프링 부트에 JSON 데이터를 보냅니다... ({file_path})")
                        post_response = post_json(file_path, year_month)
                        if post_response:
                            # 해시 파일 업데이트
                            save_hash_to_file(hash_file_path, current_hash)
                            files_processed += 1
                        else:
                            logger.error("Spring Boot에 Json 보내기 실패")
                            break

                        # 지정한 횟수만큼 파일 처리했으면 종료
                        if files_processed >= num_files_to_process:
                            break

            # 지정한 횟수만큼 파일 처리했으면 종료
            if files_processed >= num_files_to_process:
                break

        return jsonify({"/python/stock/pull": f"Success. Processed {files_processed} files"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500