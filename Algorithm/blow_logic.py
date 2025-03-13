"""剔除逻辑"""

import sys
import traceback

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from Log.logger import LoggerManager

class BlowLogic:
    def __init__(self, image_encoder_queue,blow_queue):
        ecal_core.initialize(sys.argv, "Encoder Value Subscriber")
        sub = StringSubscriber("encoder_topic")
        sub.set_callback(self.callback)
        self.logger = LoggerManager.get_logger()
        self.image_encoder_queue = image_encoder_queue
        self.blow_queue=blow_queue
        self.msg = 0
        self.boundary = 134640  # 14400一圈编码器 20cm  121680

    def detect_blow(self):
        while True:
            try:
                if not self.image_encoder_queue.empty():
                    encoder_value = self.image_encoder_queue.get()
                    while True:
                        now_encoder_value = int(self.msg)
                        if now_encoder_value - encoder_value > self.boundary:
                            self.logger.info(f"编码器差值：{now_encoder_value}-{encoder_value}={now_encoder_value-encoder_value}")
                            self.blow_queue.put("1")
                            # print(time.time(),"--send")
                            break
                        if now_encoder_value < encoder_value:
                            if now_encoder_value + (6553565535 - encoder_value) > self.boundary:
                                # print(encoder_value - now_encoder_value)
                                self.blow_queue.put("1")
                                # print(time.time(), "--send")
                                break
            except Exception as e:
                error_message = str(e)  # 错误信息
                tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
                filename, line, func, text = tb[-1]  # 获取最后一条错误信息
                self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def callback(self, topic_name, msg, time):
        self.msg = msg


def blow(image_encoder_queue,blow_queue):
    blow_logic = BlowLogic(image_encoder_queue,blow_queue)
    blow_logic.detect_blow()
