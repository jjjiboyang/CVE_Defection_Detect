import time
import traceback
from threading import Thread
from Log.logger import LoggerManager
import sys
import modbus_tk.defines as csd
import modbus_tk.modbus_rtu as rtu
import serial
from ecal.core.publisher import StringPublisher
import ecal.core.core as ecal_core


class SignalLight:
    def __init__(self, light_queue, blow_queue):
        self.logger = LoggerManager.get_logger("IO_logger")
        self.read_thread = None
        self.light_queue = light_queue
        self.blow_queue = blow_queue

        try:
            self.master = rtu.RtuMaster(serial.Serial(port="com7", baudrate=115200, parity="N",bytesize=8,stopbits=1))
            self.master.set_timeout(5.0)
            self.master.set_verbose(False)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def ready(self):
        try:
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=2, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=3, output_value=1)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=4, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=5, output_value=0)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def run(self):
        try:
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=2, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=3, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=4, output_value=1)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def stop(self):
        try:
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=2, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=3, output_value=1)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=4, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=5, output_value=0)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def alarm(self):
        try:
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=2, output_value=1)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=5, output_value=1)
            time.sleep(0.5)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=5, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=2, output_value=0)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def close(self):
        try:
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=3, output_value=0)
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=4, output_value=0)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def start_blow(self):
        try:
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=6, output_value=1)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def stop_blow(self):
        try:
            self.master.execute(1, csd.WRITE_SINGLE_COIL, starting_address=6, output_value=0)
        except Exception as e:
            error_message = str(e)  # 错误信息
            tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
            filename, line, func, text = tb[-1]  # 获取最后一条错误信息
            self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")

    def blow_long(self):
        ecal_core.initialize(sys.argv, "IO Value Publisher")
        pub = StringPublisher("io_topic")
        ti_chu = 0
        last_red0 = 0
        flag = 1
        while ecal_core.ok():
            try:
                if not self.light_queue.empty():
                    data = self.light_queue.get()
                    if data == "ready":
                        self.ready()
                    elif data == "close":
                        self.close()
                    elif data == "run":
                        self.run()
                    elif data == "stop":
                        self.stop()
                    elif data == "alarm":
                        self.alarm_thread = Thread(target=self.alarm, daemon=True)
                        self.alarm_thread.start()
                while not self.blow_queue.empty():
                    signal = self.blow_queue.get()
                    ti_chu += int(signal)
                red = self.master.execute(1, csd.READ_DISCRETE_INPUTS, 0, 1)
                if red[0] == 1 and last_red0 == 0:
                    if ti_chu >= 1 or flag == 2:
                        if flag == 1:
                            flag = 2
                            self.light_queue.put("alarm")
                        elif flag == 2:
                            flag = 1
                        ti_chu = 0
                        last_red0 = 1
                        pub.send("剔除一根")
                        continue
                    last_red0 = 1
                    pub.send("111")
                    self.start_blow()
                if red[0] == 0 and last_red0 == 1:
                    last_red0 = 0
                    self.stop_blow()

                # print(f"{red}")

            except Exception as e:
                error_message = str(e)  # 错误信息
                tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
                filename, line, func, text = tb[-1]  # 获取最后一条错误信息
                self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")
                # 让循环继续运行，而不是直接退出
                continue

        ecal_core.finalize()

    def blow_short(self):
        ecal_core.initialize(sys.argv, "IO Value Publisher")
        pub = StringPublisher("io_topic")
        ti_chu = 0
        last_red0 = 0
        flag = 1
        while ecal_core.ok():
            try:
                if not self.light_queue.empty():
                    data = self.light_queue.get()
                    if data == "ready":
                        self.ready()
                    elif data == "close":
                        self.close()
                    elif data == "run":
                        self.run()
                    elif data == "stop":
                        self.stop()
                    elif data == "alarm":
                        self.alarm_thread = Thread(target=self.alarm, daemon=True)
                        self.alarm_thread.start()
                if not self.blow_queue.empty():
                    signal = self.blow_queue.get()
                    ti_chu += int(signal)
                # 读取吹气信号
                red = self.master.execute(1, csd.READ_DISCRETE_INPUTS, 0, 1)
                if red[0] == 1 and last_red0 == 0:
                    if ti_chu >= 1 or flag == 2:
                        if flag == 1:
                            flag = 2
                            self.light_queue.put("alarm")
                        elif flag == 2:
                            flag = 1
                        ti_chu = 0
                        self.start_blow()
                        last_red0 = 1
                        pub.send("剔除一根")
                        print("剔除")
                        continue
                    pub.send("111")
                if red[0] == 0 and last_red0 == 1:
                    last_red0 = 0
                    self.stop_blow()

                # print(f"{red}")

            except Exception as e:
                error_message = str(e)  # 错误信息
                tb = traceback.extract_tb(e.__traceback__)  # 获取 traceback 详细信息
                filename, line, func, text = tb[-1]  # 获取最后一条错误信息
                self.logger.error(f"文件: {filename},行号: {line},函数: {func},代码: {text},错误信息: {error_message}")
                # 让循环继续运行，而不是直接退出
                continue

        ecal_core.finalize()


def run_BlowLong(light_queue, blow_queue):
    signal_knife = SignalLight(light_queue, blow_queue)
    signal_knife.blow_long()


def run_BlowShort(light_queue, blow_queue):
    signal_knife = SignalLight(light_queue, blow_queue)
    signal_knife.blow_short()
