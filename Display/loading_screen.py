from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("加载中...")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)  # 无边框 & 置顶
        self.setFixedSize(350, 180)

        # 设置窗口背景颜色和圆角
        self.setStyleSheet("""
            background-color: #2E3440;  /* 深色背景 */
            border-radius: 10px;  /* 圆角 */
        """)

        layout = QVBoxLayout()

        # 标题文本
        self.label = QLabel("正在启动程序，请稍候...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("Arial", 20, QFont.Weight.Bold))  # 调整标题大小
        self.label.setStyleSheet("color: #D8DEE9;")  # 白色字体

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 让进度数值居中
        self.progress_bar.setFont(QFont("Arial", 16, QFont.Weight.Bold))  # 数字更大
        self.progress_bar.setFormat("%p%")  # 让进度条显示百分比
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4C566A;
                border-radius: 5px;
                background-color: #3B4252;
                height: 12px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #88C0D0;
                width: 10px;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        # 启动定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress = 0
        self.timer.start(50)  # 每 50 毫秒更新一次

    def update_progress(self):
        self.progress += 2  # 逐步增加进度
        self.progress_bar.setValue(self.progress)

        if self.progress >= 100:
            self.timer.stop()
            self.accept()  # 关闭加载窗口
