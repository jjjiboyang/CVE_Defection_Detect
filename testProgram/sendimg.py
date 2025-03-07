import sys
import os
import time

import cv2
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
import numpy as np
from CamGrab import datatype_pb2


class SendImage:
    def __init__(self, image_folder):
        self.image_folder = image_folder  # 图片所在文件夹
        self.encoder_value = [15644896]  # 存储编码器值

        # 初始化 eCAL
        ecal_core.initialize(sys.argv, "Encoder Value Subscriber")
        sub = StringSubscriber("encoder_topic")
        sub.set_callback(self.callback)

    def callback(self, topic_name, msg, time):
        """接收编码器值"""
        self.encoder_value[0] = int(msg)

    def StartGrab(self):
        """从本地读取图片并发送"""
        ecal_core.initialize(sys.argv, "Grab Image Publisher")
        pub = ecal_core.publisher(f'defect_detection_topic_2')

        # 获取文件夹中的所有图片
        image_files = [f for f in os.listdir(self.image_folder) if f.endswith(".bmp")]
        if not image_files:
            print("No .bmp images found in the folder!")
            return

        for image_name in image_files:
            image_path = os.path.join(self.image_folder, image_name)
            print(f"Processing image: {image_path}")

            # 读取图片
            img_np = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img_np is None:
                print(f"Failed to read {image_path}")
                continue

            # 获取图片尺寸
            height, width = img_np.shape[:2]

            # 编码为字节流
            is_success, buffer = cv2.imencode('.bmp', img_np)
            if not is_success:
                print(f"Failed to encode {image_path}")
                continue

            # 创建 Protobuf 消息
            image_msg = datatype_pb2.ImageParameters()
            image_msg.data = buffer.tobytes()
            image_msg.width = width
            image_msg.height = height
            image_msg.encoder_value = self.encoder_value[0]  # 使用最新编码器值
            image_msg.timestamp = 1733268329529  # 模拟时间戳
            image_msg.filename = image_name  # 记录文件名

            # 发送消息
            serialized_message = image_msg.SerializeToString()
            pub.send(serialized_message)
            print(f"Sent image: {image_name}")

            time.sleep(5)

        print("All images processed.")


def camera_grab_from_folder(folder_path):
    """从本地文件夹读取图片并发送"""
    cam = SendImage(folder_path)
    cam.StartGrab()


if __name__ == '__main__':
    folder_path = "C:/Users/16146\Desktop/testimage"  # 设定本地存放图片的文件夹
    camera_grab_from_folder(folder_path)
