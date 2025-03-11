import sys
import ecal.core.core as ecal_core
import modbus_tk.defines as csd
import modbus_tk.modbus_rtu as rtu
import serial
from ecal.core.publisher import StringPublisher
from Log.logger import LoggerManager


class PubSignal:
    def __init__(self):
        self.logger = LoggerManager.get_logger()
        try:
            self.master_encoder = rtu.RtuMaster(serial.Serial(port="com8", baudrate=115200, parity="N"))
            self.master_encoder.set_timeout(5.0)
            self.master_encoder.set_verbose(False)
        except Exception as e:
            self.logger.error(e)

    def Encoder(self):
        ecal_core.initialize(sys.argv, "Encoder Value Publisher")
        pub = StringPublisher("encoder_topic")

        while ecal_core.ok():
            try:
                # 读取保存
                red = self.master_encoder.execute(1, csd.READ_HOLDING_REGISTERS, 16, 2)
            except Exception as e:
                self.logger.error(e)
                break
            pub.send(str(red[1]).zfill(5) + str(red[0]).zfill(5))
        ecal_core.finalize()


def run_SignalGrab():
    pub_signal = PubSignal()
    pub_signal.Encoder()


if __name__ == "__main__":
    run_SignalGrab()
