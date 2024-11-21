import sys
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, Qt, QTime


class StatusInfoWidgetLeft(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化
        self.start_time = QTime.currentTime()
        self.pixmap_run = QPixmap(":title_icon/icon/正在运行.png")
        self.pixmap_stop = QPixmap(":title_icon/icon/停止运行.png")
        self.elapsed_time = 0
        self.running = False

        # 创建标签
        self.current_time_label = QLabel("北京时间:  ")
        self.start_time_label = QLabel("开始时间:  00:00:00")
        self.duration_label = QLabel("持续时间:  00:00:00")
        self.io_status_label = QLabel(f"IO状态: 未在接收")
        self.pixmap_label = QLabel()
        self.pixmap_label.setPixmap(self.pixmap_stop)
        self.pixmap_label.setMaximumSize(20, 20)
        self.pixmap_label.setScaledContents(True)

        self.current_time_label.setStyleSheet("font-size:17px;")
        self.start_time_label.setStyleSheet("font-size:17px;")
        self.duration_label.setStyleSheet("font-size:17px;")
        self.io_status_label.setStyleSheet("font-size:17px;")

        # 设置标签的最小尺寸和对齐方式
        labels = [
            self.current_time_label,
            self.start_time_label,
            self.duration_label,
            self.io_status_label,
        ]

        for label in labels:
            label.setMinimumSize(0, 30)
            label.setMaximumSize(10000, 30)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # IO状态
        layoutH = QHBoxLayout()
        layoutH.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layoutH.addWidget(self.io_status_label)
        layoutH.addWidget(self.pixmap_label)

        # 创建垂直布局并添加标签
        layout = QVBoxLayout(self)
        layout.addWidget(self.current_time_label)
        layout.addWidget(self.start_time_label)
        layout.addWidget(self.duration_label)
        layout.addLayout(layoutH)

        # 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_duration)
        self.timer.setInterval(1000)  # 每秒更新

        # 定时器用于更新标签
        self.timerNow = QTimer()
        self.timerNow.timeout.connect(self.update_current_time_label)
        self.timerNow.setInterval(1000)  # 每秒更新一次
        self.timerNow.start()

    def start_timing(self):
        if not self.running:  # 确保计时器没有在运行
            self.start_time = QTime.currentTime()
            self.running = True
            self.timer.start()  # 启动计时器
            self.update_start_time_label()  # 更新开始时间标签
            self.io_status_label.setText(f"IO状态: 正在接收")
            self.pixmap_label.setPixmap(self.pixmap_run)

    def stop_timing(self):
        if self.running:  # 确保计时器正在运行
            self.running = False
            self.timer.stop()  # 停止计时器
            self.io_status_label.setText(f"IO状态: 停止接收")
            self.pixmap_label.setPixmap(self.pixmap_stop)

    def update_duration(self):
        """只在计时器运行时更新持续时间。"""
        if self.running:
            self.elapsed_time += 1
            elapsed_str = QTime(0, 0).addSecs(self.elapsed_time).toString("hh:mm:ss")
            self.duration_label.setText(f"持续时间:  {elapsed_str}")

    def update_start_time_label(self):
        self.start_time_label.setText(f"开始时间:  {self.start_time.toString('hh:mm:ss')}")

    def update_current_time_label(self):
        self.current_time_label.setText(f"北京时间:  {(QTime.currentTime()).toString('hh:mm:ss')}")
