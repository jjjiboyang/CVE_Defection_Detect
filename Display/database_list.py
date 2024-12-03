from threading import Thread
import lmdb
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ImageDisplayWidget:
    def __init__(self, ui, message_queue):
        super().__init__()
        self.ui = ui
        self.message_queue = message_queue
        self.db_path = "./data_lmdb"

        self.load_data(self.db_path)
        self.ui.listWidget.itemClicked.connect(self.display_image)
        if self.ui.listWidget.count() > 0:
            self.ui.listWidget.setCurrentRow(0)

        Thread(target=self.add_image_entry, daemon=True).start()

    def load_data(self, db_path):
        with lmdb.open(db_path) as env:
            with env.begin() as txn:
                cursor = txn.cursor()
                # 反向遍历游标，从最新记录开始
                cursor.last()  # 定位到数据库的最后一条记录
                latest_keys = []

                for i, (key, _) in enumerate(cursor):
                    if i >= 50:  # 只获取最新的50条记录
                        break
                    latest_keys.append(key.decode())

                # 反转列表，因为是从最新到最旧插入
                latest_keys.reverse()

                for key in latest_keys:
                    self.ui.listWidget.insertItem(0, key)

                # 加载最后一条图像进行显示
                if latest_keys:
                    last_key = latest_keys[-1]  # 获取最新的键
                    with lmdb.open(self.db_path) as env:
                        with env.begin() as txn:
                            image_data = txn.get(last_key.encode())
                            if image_data:
                                pixmap = QPixmap()
                                pixmap.loadFromData(image_data)
                                scaled_pixmap = pixmap.scaled(self.ui.label_12.size() * 20,
                                                              Qt.AspectRatioMode.KeepAspectRatio,
                                                              Qt.TransformationMode.SmoothTransformation)
                                self.ui.label_12.setPixmap(scaled_pixmap)

    def display_image(self, item):
        key = item.text()
        self.display_image_by_key(key)

    def display_image_by_key(self, key):
        with lmdb.open(self.db_path) as env:
            with env.begin() as txn:
                image_data = txn.get(key.encode())
                if image_data:
                    pixmap = QPixmap()
                    pixmap.loadFromData(image_data)
                    scaled_pixmap = pixmap.scaled(self.ui.label_12.size(), Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)
                    self.ui.label_12.setPixmap(scaled_pixmap)

    def add_image_entry(self):
        while True:
            if not self.message_queue.empty():
                key = self.message_queue.get()
                # 更新 UI
                if self.ui.listWidget.count() >= 50:
                    self.ui.listWidget.takeItem(self.ui.listWidget.count() - 1)  # 删除最旧的项目

                # 在最上方添加新的项目
                self.ui.listWidget.insertItem(0, key)
