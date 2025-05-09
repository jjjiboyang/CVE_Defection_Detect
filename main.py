"""Main Procedure"""

import multiprocessing
from multiprocessing import Process
import os
import sys
import shutil
import time
from datetime import datetime
from PySide6.QtWidgets import QApplication
from Display.main_window import MainWindow
from qt_material import apply_stylesheet
from Display.loading_screen import LoadingScreen
from Log.logger import LoggerManager


def log_listener(log_queue):
    logger = LoggerManager.get_logger()
    logged_errors = set()  # 用于判重

    while True:
        data = log_queue.get()
        if data == "STOP":
            break
        error_message, detail_message = data
        if error_message not in logged_errors:
            logged_errors.add(error_message)
            logger.error(detail_message)  # 只写一次完整日志

if __name__ == "__main__":
    multiprocessing.freeze_support()

    if not os.path.exists("C:/Windows/software.config"):
        exit(0)
    # if os.path.isfile("log.txt"):
    #     os.remove("log.txt")
    # if os.path.isdir("./All_Images"):
    #     shutil.rmtree("./All_Images")
    # if os.path.isdir("./data_lmdb"):
    #     shutil.rmtree("./data_lmdb")

    # 创建保存日志的目录
    os.makedirs("./log", exist_ok=True)
    log_queue = multiprocessing.Queue()
    listener = Process(target=log_listener, args=(log_queue,),daemon=True)
    listener.start()

    # 创建以当前日期命名的文件夹
    FOLDER = f"./All_Images/{(datetime.now().strftime('%Y-%m-%d'))}"
    # 创建文件夹保存所有图片
    os.makedirs(FOLDER, exist_ok=True)

    # 创建保存缺陷小图的文件夹
    os.makedirs(f"{FOLDER}/out_long", exist_ok=True)
    os.makedirs(f"{FOLDER}/out_jingyuan", exist_ok=True)
    os.makedirs(f"{FOLDER}/out_black", exist_ok=True)
    os.makedirs(f"{FOLDER}/out_noblack", exist_ok=True)
    os.makedirs(f"{FOLDER}/out_continue", exist_ok=True)
    os.makedirs(f"{FOLDER}/out_water", exist_ok=True)
    # 创建保存原图的文件夹
    os.makedirs(f"{FOLDER}/defect_images", exist_ok=True)

    app = QApplication(sys.argv)

    # 显示加载界面
    loading_screen = LoadingScreen()
    loading_screen.exec()  # 运行加载界面（会阻塞，直到加载完成）

    # 继续加载主界面
    window = MainWindow(log_queue)

    extra = {

        # Button colors
        'danger': '#dc3545',
        'warning': '#ffc107',
        'success': '#17a2b8',

        # Font
        'font_family': 'Roboto',
        'font_size': 12,
    }
    apply_stylesheet(app, 'dark_teal.xml', invert_secondary=True, extra=extra)

    window.show()

    sys.exit(app.exec())
