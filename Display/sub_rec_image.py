import sys
import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal
import CamGrab.datatype_pb2 as datatype_pb2
import ecal.core.core as ecal_core
from Log.logger import logger_config


class EcalReceiverThread(QThread):
    image_received_1 = Signal(np.ndarray)  # Signal to send the image
    image_received_2 = Signal(np.ndarray)  # Signal to send the image

    def __init__(self):
        super().__init__()
        self.looger = logger_config()
        self.running = False

    def run(self):
        ecal_core.initialize(sys.argv, "Python Protobuf Subscriber")
        sub_1 = ecal_core.subscriber('defect_detection_topic_1')
        sub_2 = ecal_core.subscriber('defect_detection_topic_2')
        sub_1.set_callback(self.callback_1)
        sub_2.set_callback(self.callback_2)

    def callback_1(self, topic_name, msg, time):
        if self.running == True:
            received_message = datatype_pb2.ImageParameters()
            received_message.ParseFromString(msg)
            np_arr = np.frombuffer(received_message.data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
            self.image_received_1.emit(img)

    def callback_2(self, topic_name, msg, time):
        if self.running == True:
            received_message = datatype_pb2.ImageParameters()
            received_message.ParseFromString(msg)
            np_arr = np.frombuffer(received_message.data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
            self.image_received_2.emit(img)

    def start_receive(self):
        self.running = True

    def stop_receive(self):
        self.running = False
