from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class StatusBar:
    def __init__(self, ui):
        self.ui = ui
        self.ui.statusbar.setStyleSheet("font-size: 15px;")
        self.setpermanent()

    def setpermanent(self):
        # 添加一个显示永久信息的标签控件
        self.info = QLabel()
        self.info.setText('北京康视杰智能科技有限公司')
        self.info.setStyleSheet("font-size: 15px;")
        self.info.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.info.setContentsMargins(0, 0, 10, 0)
        self.ui.statusbar.addPermanentWidget(self.info)

    def show(self, message):
        self.ui.statusbar.showMessage(message)
