import logging
import os
from datetime import datetime


class LoggerManager:
    _logger = None  # 静态变量

    @staticmethod
    def get_logger():
        """ 获取全局 logger（单例模式） """
        if LoggerManager._logger is None:
            log_dir = "./log"
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.txt")

            logger = logging.getLogger("global_logger")
            logger.setLevel(logging.DEBUG)

            # 避免重复添加 Handler
            if not logger.handlers:
                file_handler = logging.FileHandler(log_path, encoding="utf-8")
                console_handler = logging.StreamHandler()
                formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

                file_handler.setFormatter(formatter)
                console_handler.setFormatter(formatter)

                logger.addHandler(file_handler)
                logger.addHandler(console_handler)

            LoggerManager._logger = logger

        return LoggerManager._logger
