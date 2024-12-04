import os
from PySide6.QtWidgets import QLabel, QVBoxLayout, QLineEdit, QWidget, QGraphicsView, QPushButton, QApplication
from PySide6.QtCore import Qt, QThread, Signal, Slot, QRunnable, QThreadPool
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
import sys
import CamGrab.datatype_pb2 as datatype_pb2
from Log.logger import logger_config

sys.path.append('data_json.py')


class DefectNumber(QThread):
    defect_type_signal = Signal(str)  # 缺陷的种类个数

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

        self.defect_type_signal.emit(received_message.defect_type)


class ProductNumber(QThread):
    produced_number_signal = Signal(int)  # 生产产量
    blow_number_signal = Signal(int)   # 剔除的数量

    def __init__(self):
        super().__init__()
        self.logger = logger_config()

    def run(self):
        ecal_core.initialize(sys.argv, "IO Value Subscriber")
        sub = StringSubscriber('io_topic')
        sub.set_callback(self.callback)

    def callback(self, topic_name, msg, time):
        if msg == "111":
            self.produced_number_signal.emit(1)
        else:
            self.blow_number_signal.emit(1)


class ProductInfoWidgetRight(QWidget):
    def __init__(self, graphics_view):
        super().__init__()
        # 初始化
        self.defects_type1_count,self.defects_type2_count,self.defects_type3_count,self.defects_type4_count=0,0,0,0
        self.blow_count = 0
        self.produced_number_sum = 0
        self.bad_rate = 0
        self.graphics_view = graphics_view
        self.running = False

        # 创建各个标签
        self.produced_number_label = QLabel(f"实时产量: {self.produced_number_sum}")
        self.rejection_count_label = QLabel(f"缺陷产品数: {self.blow_count}")
        self.normal_rate_label = QLabel(f"产品不合格率: {self.bad_rate}%")
        self.defects_type1_label = QLabel(f"长条划痕缺陷数量: {self.defects_type1_count}")
        self.defects_type2_label = QLabel(f"晶圆水斑缺陷数量: {self.defects_type2_count}")
        self.defects_type3_label = QLabel(f"糊料黑点缺陷数量: {self.defects_type3_count}")
        self.defects_type4_label = QLabel(f"连续晶圆缺陷数量: {self.defects_type4_count}")

        self.produced_number_label.setStyleSheet("font-size:17px;")
        self.defects_type1_label.setStyleSheet("font-size:17px;")
        self.normal_rate_label.setStyleSheet("font-size:17px;")
        self.rejection_count_label.setStyleSheet("font-size:17px;")
        self.defects_type2_label.setStyleSheet("font-size:17px;")
        self.defects_type3_label.setStyleSheet("font-size:17px;")
        self.defects_type4_label.setStyleSheet("font-size:17px;")

        # 设置其他标签的最小尺寸和对齐方式
        labels = [
            self.produced_number_label,
            self.normal_rate_label,
            self.defects_type1_label,
            self.rejection_count_label,
            self.defects_type2_label,
            self.defects_type3_label,
            self.defects_type4_label,
        ]
        for label in labels:
            label.setMinimumSize(0, 30)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 创建垂直布局并添加标签
        layout = QVBoxLayout(self)
        layout.addWidget(self.produced_number_label)
        layout.addWidget(self.rejection_count_label)
        layout.addWidget(self.normal_rate_label)
        layout.addWidget(self.defects_type1_label)
        layout.addWidget(self.defects_type2_label)
        layout.addWidget(self.defects_type3_label)
        layout.addWidget(self.defects_type4_label)

        self.defect_num = DefectNumber()
        self.defect_num.defect_type_signal.connect(self.update_counts)
        self.defect_num.start()

        self.product_num = ProductNumber()
        self.product_num.produced_number_signal.connect(self.update_produced_number)
        self.product_num.blow_number_signal.connect(self.update_blow_number)
        self.product_num.start()

    # def start_running(self):
    #     if not self.running:  # 确保计时器没有在运行
    #         self.running = True
    #         self.defect_num.start()
    #         self.product_num.start()

    # def stop_running(self):
    #     if self.running:  # 确保计时器正在运行
    #         self.running = False
    #         self.defect_num.terminate()
    #         self.product_num.terminate()

    def stop_update_num(self):
        self.defect_num.terminate()
        self.product_num.terminate()

    def update_counts(self, defect_type):
        for i in defect_type:
            if i == "1":
                self.defects_type1_count += 1
                self.defects_type1_label.setText(f"长条划痕缺陷数量: {self.defects_type1_count}")
            elif i == "2":
                self.defects_type2_count += 1
                self.defects_type2_label.setText(f"晶圆水斑缺陷数量: {self.defects_type2_count}")
            elif i == "3":
                self.defects_type3_count += 1
                self.defects_type3_label.setText(f"糊料黑点缺陷数量: {self.defects_type3_count}")
            elif i == "4":
                self.defects_type4_count += 1
                self.defects_type4_label.setText(f"连续晶圆缺陷数量: {self.defects_type4_count}")


    def update_blow_number(self, blow_num):
        self.blow_count += blow_num
        self.rejection_count_label.setText(f"剔除数量: {self.blow_count}")

    def update_produced_number(self, product_num):
        self.produced_number_sum += 1
        self.bad_rate = round(self.blow_count / self.produced_number_sum, 5)
        self.produced_number_label.setText(f"实时产量: {self.produced_number_sum}")
        self.normal_rate_label.setText(f"产品不合格率: {self.bad_rate}")
