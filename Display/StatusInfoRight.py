import sys
import time
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QThread, Signal
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber


class EncoderThread(QThread):
    encoder_data_signal = Signal(str)  # 用于发送编码器数据

    def run(self):
        ecal_core.initialize(sys.argv, "Encoder Value Subscriber")
        sub = StringSubscriber("encoder_topic")
        sub.set_callback(self.callback)

    def callback(self, topic_name, msg, time):
        self.encoder_data_signal.emit(msg)


class ShowFPSThread(QThread):
    fps_signal = Signal(int, int)

    def __init__(self):
        super().__init__()
        self.graphicsView_count_1 = 0
        self.graphicsView_count_2 = 0
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            time.sleep(1)
            # 每秒发射信号，传递两个计数值
            self.fps_signal.emit(self.graphicsView_count_1, self.graphicsView_count_2)
            # 重置计数
            self.graphicsView_count_1 = 0
            self.graphicsView_count_2 = 0

    def stop(self):
        self.running = False

    def increment_view_1(self):
        if self.running:
            self.graphicsView_count_1 += 1

    def increment_view_2(self):
        if self.running:
            self.graphicsView_count_2 += 1


class StatusInfoWidgetRight(QWidget):
    def __init__(self):
        super().__init__()

        # 保存外部变量
        self.time_front = None
        self.low_front = -1
        self.high_front = -1
        self.distance_var = 0
        self.speed_var = 0

        # 创建标签
        self.distance_label = QLabel(f"运行距离(m): 0")
        self.speed_label = QLabel(f"运行速度(m/min): {self.speed_var}")
        self.FPS_label = QLabel(f"显示帧率:  0帧/秒  0帧/秒")
        self.encoder_label = QLabel(f"编码器：")

        self.distance_label.setStyleSheet("font-size:17px;")
        self.speed_label.setStyleSheet("font-size:17px;")
        self.FPS_label.setStyleSheet("font-size:17px;")
        self.encoder_label.setStyleSheet("font-size:17px;")

        # 设置标签的最小尺寸和对齐方式
        labels = [
            self.distance_label,
            self.speed_label,
            self.FPS_label,
            self.encoder_label,
        ]

        for label in labels:
            label.setMinimumSize(0, 30)
            label.setMaximumSize(10000, 30)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 创建垂直布局并添加标签
        layout = QVBoxLayout(self)
        layout.addWidget(self.distance_label)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.FPS_label)
        layout.addWidget(self.encoder_label)

        # 启动编码器线程
        self.encoder_thread = EncoderThread()
        self.encoder_thread.encoder_data_signal.connect(self.update_encoder)  # 连接信号槽
        self.encoder_thread.encoder_data_signal.connect(self.distance_speed)
        self.encoder_thread.start()

        # 初始化计算帧率线程
        self.image_set_counter = ShowFPSThread()
        self.image_set_counter.fps_signal.connect(self.update_FPS)
        self.image_set_counter.start()

    def update_1(self):
        self.image_set_counter.increment_view_1()

    def update_2(self):
        self.image_set_counter.increment_view_2()

    def update_FPS(self, fps1, fps2):
        self.FPS_label.setText(f"显示帧率:  {fps1}帧/秒  {fps2}帧/秒")

    def distance_speed(self, data):  # 在此项目中编码器的值是递减的
        high = int(data[0:5])
        low = int(data[5::])
        if self.high_front == -1:  # 程序开始时，high_front还没有被赋值
            self.high_front = high  # 初始化赋值
            self.low_front = low  # 初始化赋值
            self.time_front = time.time()  # 初始化赋值
            return

        if time.time() - self.time_front >= 1:
            high_increment = self.high_front - high
            if high_increment == 0:
                increase = self.low_front - low
            elif high_increment < 0:
                increase = self.low_front + (65535 - low)
            else:
                increase = (high_increment - 1) * 100000 + self.low_front + (65535 - low)
            self.speed_var = increase / 14400 * 0.223 * 60
            self.distance_var += self.speed_var / 60
            self.distance_label.setText(f"运行距离(m): {round(self.distance_var, 1)}")
            self.speed_label.setText(f"运行速度(m/min): {round(self.speed_var, 1)}")  # 更新速度显示
            self.high_front = high
            self.low_front = low
            self.time_front = time.time()

    def update_encoder(self, data):
        # 更新编码器标签
        self.encoder_label.setText(f"编码器：{data}")

    def close_window(self):
        self.image_set_counter.terminate()
        self.encoder_thread.terminate()
