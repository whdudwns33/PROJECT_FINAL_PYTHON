# logger_config.py
import logging
import os

def config_logger(log_file):
    log_folder = os.path.dirname(log_file)
    os.makedirs(log_folder, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 파일 핸들러 설정
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 로거 설정
    logger = logging.getLogger(log_file)  # 로거 이름을 지정
    logger.setLevel(logging.INFO)

    # 기존에 설정된 핸들러가 있다면 중복 추가하지 않도록 체크
    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger
