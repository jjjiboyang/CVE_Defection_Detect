from multiprocessing import Process

from PySide6.QtWidgets import QButtonGroup
from EncoderIO.SignalLight import run_BlowLong
from EncoderIO.SignalLight import run_BlowShort


class CheckBox:
    def __init__(self, ui, light_queue,blow_queue,log_queue):
        super().__init__()
        self.ui = ui
        self.light_queue = light_queue
        self.log_queue = log_queue
        self.blow_queue = blow_queue
        self.blow_signal = Process(target=run_BlowLong, args=(self.light_queue,self.blow_queue,self.log_queue), daemon=True)
        self.blow_signal.start()

        '''CheckBox'''
        self.ui.label_5.setStyleSheet("font-size: 17px;")
        self.ui.label_6.setStyleSheet("font-size: 17px;")
        self.ui.label_7.setStyleSheet("font-size: 17px;")
        self.ui.checkBox_1.setStyleSheet("font-size:16px;")
        self.ui.checkBox_2.setStyleSheet("font-size:16px;")
        self.ui.checkBox_3.setStyleSheet("font-size:16px;")
        self.ui.checkBox_4.setStyleSheet("font-size:16px;")
        self.ui.checkBox_5.setStyleSheet("font-size:16px;")
        self.ui.checkBox_6.setStyleSheet("font-size:16px;")
        self.ui.checkBox_9.setStyleSheet("font-size:16px;")
        self.ui.checkBox_10.setStyleSheet("font-size:16px;")
        self.ui.ButtonGroup1 = QButtonGroup()
        self.ui.ButtonGroup1.addButton(self.ui.checkBox_3)
        self.ui.ButtonGroup1.addButton(self.ui.checkBox_4)
        self.ui.ButtonGroup2 = QButtonGroup()
        self.ui.ButtonGroup2.addButton(self.ui.checkBox_5)
        self.ui.ButtonGroup2.addButton(self.ui.checkBox_6)

    def on_checkbox5_changed(self, state):
        if state == 2:  # Checked
            self.blow_signal.terminate()
            self.blow_signal = Process(target=run_BlowLong, args=(self.light_queue,self.blow_queue,self.log_queue), daemon=True)
            self.blow_signal.start()

    def on_checkbox6_changed(self, state):
        if state == 2:
            self.blow_signal.terminate()
            self.blow_signal = Process(target=run_BlowShort, args=(self.light_queue,self.blow_queue,self.log_queue), daemon=True)
            self.blow_signal.start()
