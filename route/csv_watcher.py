from common.logger_config import config_logger
import hashlib
import os

# 로거 설정
logger = config_logger('logs/app.log')

def get_file_hash(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        return hashlib.md5(file_content).hexdigest()

def is_file_changed(file_path, last_hash):
    current_hash = get_file_hash(file_path)
    return current_hash != last_hash

def get_last_hash_from_file(file_path):
    try:
        with open(file_path, 'r') as hash_file:
            return hash_file.read().strip()
    except FileNotFoundError:
        return None

def save_hash_to_file(file_path, hash_value):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as hash_file:
        hash_file.write(hash_value)

def check_all_csv_files(directory_path, hashes_directory):
    # 디렉토리 내의 모든 파일 확인
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            # 파일 확장자가 .csv 인지 확인
            if file_name.lower().endswith(".csv"):
                file_path = os.path.join(root, file_name)

                # 해시 파일 저장 경로
                hash_file_path = os.path.join(hashes_directory, file_path.replace(directory_path, "") + ".hash")

                last_hash = get_last_hash_from_file(hash_file_path)
                current_hash = get_file_hash(file_path)

                if last_hash is None or current_hash != last_hash:
                    logger.info(f"hash값이 변경되었습니다! 스프링 부트에 JSON 데이터를 보냅니다... ({file_path})")
                    # Spring Boot에 데이터 전송하는 코드 추가

                    # 해시 파일 업데이트
                    save_hash_to_file(hash_file_path, current_hash)
