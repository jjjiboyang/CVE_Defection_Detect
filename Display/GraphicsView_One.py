from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSizePolicy
from PySide6.QtGui import QWheelEvent, QPainter, QTransform, QImage, QPixmap
from PySide6.QtCore import Qt, QPointF, QSize


class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Expanding
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # 启用拖动模式
        self.setRenderHint(QPainter.Antialiasing)  # 启用抗锯齿
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)  # 缩放从鼠标位置开始
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)  # 窗口大小调整从鼠标位置开始
        self.scale_factor = 1.15  # 设置缩放因子
        self.current_scale = 1.0  # 当前缩放比例

        # 隐藏水平和垂直滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def wheelEvent(self, event: QWheelEvent):
        """通过滚轮事件来实现缩放"""
        if event.angleDelta().y() > 0:  # 滚轮向前滚动
            self.scale(self.scale_factor, self.scale_factor)
            self.current_scale *= self.scale_factor
        else:  # 滚轮向后滚动
            self.scale(1 / self.scale_factor, 1 / self.scale_factor)
            self.current_scale /= self.scale_factor

    def resizeEvent(self, event):
        """在窗口大小调整时自动调整图片大小，不保留宽高比"""
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.IgnoreAspectRatio)
        super().resizeEvent(event)

    def fitInView(self, rect, flags=Qt.AspectRatioMode.IgnoreAspectRatio):
        super().fitInView(rect, flags)
        self.initial_transform = self.transform()  # 保存自适应铺满的状态

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 恢复到自适应铺满的状态
            self.setTransform(self.initial_transform)
        else:
            super().mousePressEvent(event)  # 调用父类的鼠标点击事件处理

    def set_image(self, img):
        # 将 OpenCV 图像转换为 QImage
        height, width = img.shape
        qimage = QImage(img.data, width, height, width, QImage.Format.Format_Grayscale8)
        # 将 QImage 转换为 QPixmap
        pixmap = QPixmap.fromImage(qimage)
        # 加载图片并将其添加到场景中
        scene1 = QGraphicsScene()
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene1.addItem(pixmap_item)
        # 设置 QGraphicsView 的场景
        self.setScene(scene1)
        # 设置场景大小为图像的边界大小
        self.setSceneRect(pixmap_item.boundingRect())
        # 应用当前缩放比例，保持视图的缩放状态
        self.setTransform(QTransform().scale(self.current_scale, self.current_scale))
