# log_config.py
import logging

def setup_logging():
    logging.basicConfig(
        filename='./logs/shitposting_logs.log',
        encoding='utf-8',
        format='%(asctime)s %(levelname)s: %(message)s',
        level=logging.INFO
    )