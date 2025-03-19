import logging
import os
from datetime import datetime

class LoggerManager:
    _loggers = {}

    @staticmethod
    def get_logger(name="global_logger"):
        if name not in LoggerManager._loggers:
            log_dir = "./log"
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.txt")

            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)

            if not logger.handlers:
                file_handler = logging.FileHandler(log_path, encoding="utf-8")
                console_handler = logging.StreamHandler()
                formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                file_handler.setFormatter(formatter)
                console_handler.setFormatter(formatter)

                logger.addHandler(file_handler)
                logger.addHandler(console_handler)

            LoggerManager._loggers[name] = logger
        return LoggerManager._loggers[name]
