import os
import ecal.core.core as ecal_core
import sys
import CamGrab.datatype_pb2 as datatype_pb2
import cv2
import concurrent.futures
from Log.logger import logger_config
import numpy as np
from PySide6.QtCore import Qt, QSize, QThread, Signal, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QSizePolicy


class UpdateImage(QThread):
    img_data = Signal(np.ndarray, str)

    def __init__(self):
        super().__init__()
        self.logger = logger_config()

    def run(self):
        ecal_core.initialize(sys.argv, "Processed Image Subscriber")
        sub = ecal_core.subscriber('ProcessedImage')
        sub.set_callback(self.callback)

    def callback(self, topic_name, msg, time):
        received_message = datatype_pb2.ImageParameters()
        received_message.ParseFromString(msg)
        np_arr = np.frombuffer(received_message.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        image_filename = received_message.filename

        # 发射解码后的图像和缺陷数据
        self.img_data.emit(img, image_filename)


class ImageListView(QGraphicsView):
    def __init__(self, folder_path, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.image_spacing = 2
        self.image_items = []
        self.current_y_position = 0

        self.executor = concurrent.futures.ThreadPoolExecutor()

        # 加载文件夹中的图片
        self.load_images_from_folder(folder_path)

        # 创建并启动定时器
        self.timer_update_view = QTimer(self)
        self.timer_update_view.timeout.connect(self.update_view)
        self.timer_update_view.start(100)  # 每10毫秒更新一次视图

        self.update_image = UpdateImage()
        self.update_image.img_data.connect(self.add_image)
        self.update_image.start()

    def update_view(self):
        """更新视图，确保新添加的图片及时显示."""
        self.viewport().update()

    def load_images_from_folder(self, folder_path):
        """从指定文件夹加载图片并按照时间排序."""
        image_files = sorted(
            [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
             f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))],
            key=lambda x: os.path.getmtime(x), reverse=False)

        for image_file in image_files:
            img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                self.add_image(img, image_file)

    def add_image(self, img, filename):
        """直接接受 OpenCV 格式的图像并将其添加到视图中."""
        pixmap, img = self.process_image(img)
        self.on_image_processed(pixmap, img, filename)

    def process_image(self, img):
        """将 OpenCV 图像转换为适合显示的 QPixmap."""
        height, width = img.shape[:2]

        # 将 OpenCV 图像转换为 QImage
        q_img = QImage(img.data, width, height, width, QImage.Format.Format_Grayscale8)

        # 根据视口大小调整缩略图尺寸
        thumbnail_size = QSize(self.viewport().width(), self.viewport().height() // 4)
        pixmap = QPixmap.fromImage(q_img).scaled(thumbnail_size, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)

        return pixmap, img

    def on_image_processed(self, pixmap, original_img, filename):
        """当图像处理完成后，将图像添加到场景中."""
        # 创建 QGraphicsPixmapItem 并将原始图像数据存储在其中
        pixmap_item = QGraphicsPixmapItem(pixmap)
        pixmap_item.setData(0, original_img)
        pixmap_item.setData(1, filename)  # 存储文件名

        # 将图片插入到最上方
        self.image_items.insert(0, pixmap_item)
        self.scene.addItem(pixmap_item)

        # 更新图片位置
        self.current_y_position = 0
        for item in self.image_items:
            target_width = self.viewport().width()
            target_height = self.viewport().height() // 4
            item.setPos(0, self.current_y_position)
            self.current_y_position += target_height + self.image_spacing

        # 更新场景的范围以匹配内容
        self.scene.setSceneRect(0, 0, self.viewport().width(), self.current_y_position)

        self.update_view()

    def resizeEvent(self, event):
        """在窗口大小调整时更新所有图片项的位置和大小."""
        self.current_y_position = 0  # 重置 y 位置
        for item in self.image_items:
            target_width = self.viewport().width()
            target_height = self.viewport().height() // 4
            pixmap = item.pixmap().scaled(target_width, target_height, Qt.AspectRatioMode.IgnoreAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            item.setPixmap(pixmap)
            item.setPos(0, self.current_y_position)
            self.current_y_position += target_height + self.image_spacing

        self.scene.setSceneRect(0, 0, self.viewport().width(), self.current_y_position)
        super().resizeEvent(event)

    def mouseDoubleClickEvent(self, event):
        """双击图片项时显示原始大小的图片，并允许调整窗口大小."""
        item = self.itemAt(event.pos())
        if item is not None:
            original_img = item.data(0)
            filename = item.data(1)

            # 创建一个可调整大小的窗口
            cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
            cv2.imshow(filename, original_img)

            # 允许用户通过拖拽调整窗口的大小
            cv2.resizeWindow(filename, original_img.shape[1], original_img.shape[0])

            cv2.waitKey(0)
            cv2.destroyAllWindows()
        super().mouseDoubleClickEvent(event)
