import os
import queue
import sys
from datetime import datetime
import cv2
import ecal.core.core as ecal_core
import numpy as np
import CamGrab.datatype_pb2 as datatype_pb2
import lmdb


class SaveImages:
    def __init__(self, save_choice, message_queue):
        self.save_choice = save_choice
        self.message_queue = message_queue
        self.images_queue = queue.Queue()

    def callback(self, topic_name, msg, time):
        received_message = datatype_pb2.ImageParameters()
        received_message.ParseFromString(msg)
        self.images_queue.put(received_message)

    def save(self):
        ecal_core.initialize(sys.argv, "Processed Image Subscriber")
        sub = ecal_core.subscriber('ProcessedImage')
        sub.set_callback(self.callback)
        pub = ecal_core.publisher('DisplayImage')
        while ecal_core.ok():
            if not self.images_queue.empty():
                img_msg = self.images_queue.get()
                np_arr = np.frombuffer(img_msg.data, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
                # 转换为 BGR 图像，以支持彩色绘制
                img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
                # 遍历 image_msg.regions，绘制红色矩形
                for region in img_msg.regions:
                    row1, col1, row2, col2 = region.row1, region.column1, region.row2, region.column2
                    cv2.rectangle(img_color, (col1, row1), (col2, row2), (0, 0, 255), 2)  # 红色框，线宽2
                _, img_encoded = cv2.imencode('.png', img_color)  # 或者其他格式，例如 .png
                img_msg.data = img_encoded.tobytes()  # 转换为字节流
                serialized_message = img_msg.SerializeToString()
                pub.send(serialized_message)

                if img_msg.defect_type != "0":
                    self.save_images_folder(img_color, img_msg.filename)
                self.save_images_database(img_msg.data, img_msg.timestamp)

    def save_images_database(self, image_msg_data, timestamp):
        # map_size定义最大储存容量，单位是kb，以下定义10G容量
        # env = lmdb.open("./data_lmdb", map_size=50 * 1024 * 1024 * 1024)
        env = lmdb.open("./data_lmdb", map_size= 100*1024 * 1024 * 1024)
        txn = env.begin(write=True)
        dt_object = datetime.fromtimestamp(timestamp / 1000.0)
        date_time = str(dt_object.strftime('%m-%d %H:%M:%S'))
        key_val = date_time + "  " + str(timestamp)
        self.message_queue.put(key_val)
        txn.put(key=key_val.encode(), value=image_msg_data)
        txn.commit()
        env.close()

    def save_images_folder(self, img, image_filename):
        # 创建以当前日期命名的文件夹
        folder_name = f"./All_Images/{(datetime.now().strftime('%Y-%m-%d'))}/defect_images/"
        # 创建文件夹保存所有图片
        os.makedirs(folder_name, exist_ok=True)
        # 保存图片到指定文件夹
        cv2.imwrite(image_filename, img)


def SaveImage_ecal(save_choice, message_queue):
    Save = SaveImages(save_choice, message_queue)
    Save.save()
