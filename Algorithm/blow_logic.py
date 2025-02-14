"""剔除逻辑"""

import sys
import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber


class BlowLogic:
    def __init__(self, image_encoder_queue, light_queue,blow_queue):
        ecal_core.initialize(sys.argv, "Encoder Value Subscriber")
        sub = StringSubscriber("encoder_topic")
        sub.set_callback(self.callback)
        self.image_encoder_queue = image_encoder_queue
        self.light_queue = light_queue
        self.blow_queue=blow_queue
        self.msg = 0
        self.boundary = 133920  # 14400一圈编码器 20cm  121680

    def detect_blow(self):
        while True:
            if not self.image_encoder_queue.empty():
                encoder_value = self.image_encoder_queue.get()
                # print("encoder",encoder_value)
                while True:
                    now_encoder_value = int(self.msg)
                    if now_encoder_value - encoder_value > self.boundary:
                        print(now_encoder_value - encoder_value)
                        self.light_queue.put("1")
                        # print(time.time(),"--send")
                        break
                    if now_encoder_value < encoder_value:
                        if now_encoder_value + (6553565535 - encoder_value) > self.boundary:
                            # print(encoder_value - now_encoder_value)
                            self.light_queue.put("1")
                            # print(time.time(), "--send")
                            break

    def callback(self, topic_name, msg, time):
        self.msg = msg


def blow(image_encoder_queue, light_queue,blow_queue):
    blow_logic = BlowLogic(image_encoder_queue, light_queue,blow_queue)
    blow_logic.detect_blow()
