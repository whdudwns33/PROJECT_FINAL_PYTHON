from common.logger_config import config_logger
import hashlib
import os
from route.pykrx_api.post_stock_to_controller import post_json
from common.constant import LOGGER_PATH

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


# 주어진 파일에 저장된 마지막 해시값을 읽어오는 함수입니다.
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


# 주어진 디렉토리 내의 모든 CSV 파일에 대해 해시값을 체크하는 함수입니다.
def check_all_csv_files(directory_path, hashes_directory):
    # 주어진 디렉토리 내의 모든 파일을 확인합니다.
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            # 파일 확장자가 .csv 인지 확인합니다.
            if file_name.lower().endswith(".csv"):
                file_path = os.path.join(root, file_name)

                # 현재 파일의 해시값을 계산합니다.
                current_hash = get_file_hash(file_path)

                # 해시 파일의 경로를 구성합니다.
                hash_file_path = os.path.join(hashes_directory, file_path.replace(directory_path, "") + ".hash")

                # 저장된 마지막 해시값을 가져옵니다.
                last_hash = get_last_hash_from_file(hash_file_path)

                # 저장된 해시값이 없거나 현재 해시값과 다르면 작업을 수행합니다.
                if last_hash is None or current_hash != last_hash:
                    logger.info(f"hash값이 변경되었습니다! 스프링 부트에 JSON 데이터를 보냅니다... ({file_path})")
                    # 여기에 Spring Boot에 데이터를 전송하는 코드를 추가할 수 있습니다.
                    # post_json(file_path)

                    # 해시 파일을 업데이트합니다.
                    save_hash_to_file(hash_file_path, current_hash)
