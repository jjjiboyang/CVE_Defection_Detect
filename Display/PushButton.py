
class PushButton:
    def __init__(self, ui):
        self.ui = ui

    def HideText(self):
        self.ui.Start_Button.setText("")

    def ShowText(self):
        self.ui.Start_Button.setText("开始检测")
