import sys
import traceback

import ecal.core.core as ecal_core
import modbus_tk.defines as csd
import modbus_tk.modbus_rtu as rtu
import serial
from ecal.core.publisher import StringPublisher


class PubSignal:
    def __init__(self,log_queue):
        self.log_queue = log_queue
        try:
            self.master_encoder = rtu.RtuMaster(serial.Serial(port="com8", baudrate=115200, parity="N",bytesize=8,stopbits=1))
            self.master_encoder.set_timeout(5.0)
            self.master_encoder.set_verbose(False)
        except Exception as e:
            error_message = str(e)
            tb = traceback.extract_tb(e.__traceback__)
            filename, line, func, text = tb[-1]
            detail_message = f"文件: {filename}, 行号: {line}, 函数: {func}, 代码: {text}, 错误信息: {error_message}"
            # 把错误信息+完整日志内容放进队列
            self.log_queue.put((error_message, detail_message))

    def Encoder(self):
        ecal_core.initialize(sys.argv, "Encoder Value Publisher")
        pub = StringPublisher("encoder_topic")

        while ecal_core.ok():
            try:
                # 读取保存
                red = self.master_encoder.execute(1, csd.READ_HOLDING_REGISTERS, 16, 2)
                pub.send(str(red[1]).zfill(5) + str(red[0]).zfill(5))
            except Exception as e:
                error_message = str(e)
                tb = traceback.extract_tb(e.__traceback__)
                filename, line, func, text = tb[-1]
                detail_message = f"文件: {filename}, 行号: {line}, 函数: {func}, 代码: {text}, 错误信息: {error_message}"
                # 把错误信息+完整日志内容放进队列
                self.log_queue.put((error_message, detail_message))
        ecal_core.finalize()


def run_SignalGrab(log_queue):
    pub_signal = PubSignal(log_queue)
    pub_signal.Encoder()


if __name__ == "__main__":
    run_SignalGrab()
