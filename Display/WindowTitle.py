from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

# <editor-fold desc="需要的全局变量">
RES_PATH = ':title_icon/icon/'  # 资源文件基准地址

# 标题栏尺寸集合
TITLE_BAR_HEIGHT = 30  # 标题栏高度
TITLE_BUTTON_SIZE = 25  # 标题栏按键大小
TITLE_LABEL_SIZE = 25  # 标题栏标签大小
TITLE_SPACER_WIDTH = 0  # 标题栏弹簧宽度
TITLE_BUTTON_WIDTH = 35  # 标题栏按键宽度
TITLE_BUTTON_HEIGHT = 25  # 标题栏按键高度
TITLE_ICON_MAG = 8  # 标题栏图标大小

TITLE_MIN_ICON = RES_PATH + "窗口-最小化_line.png"  # 最小化图标路径
TITLE_MAX_ICON = RES_PATH + "窗口最大化.png"  # 最大化图标路径
TITLE_CLS_ICON = RES_PATH + "关闭窗口.png"  # 关闭图标路径
TITLE_RESTORE_ICON = RES_PATH + "窗口最小化.png"  # 恢复图标路径

COLOR_DARK = "#4F5B62"  # dark主题背景色
COLOR_DARK_HOVER = "#455364"  # dark主题背景色，按键悬停颜色
COLOR_LIGHT = "#FAFAFA"  # light主题背景色
COLOR_LIGHT_HOVER = "#C0C4C8"  # light主题背景色，按键悬停颜色


# </editor-fold>


class ctQTitleBar(QWidget):
    """
    自定义标题栏：实现最大化、最小化、关闭
    """

    # 初始化
    def __init__(self, parent):
        """
        function:  初始化
              in:  parent:父窗体(为QWidget类)
             out:  None
          return:  None
          others:  Initialize
        """
        # 继承自父类
        super(ctQTitleBar, self).__init__()

        # 标题栏的父窗体
        self.parentForm = parent
        # 标题栏的主布局
        self.layoutMain = QHBoxLayout(self)
        # 去除控件间的距离
        self.layoutMain.setSpacing(0)
        self.layoutMain.setContentsMargins(0, 0, 0, 0)
        # 标题栏图标
        self.lblIcon = QLabel(self)
        # 标题栏标题
        self.lblTitle = QLabel("医用透明管材机器视觉在线检测系统V3.1.1")
        self.lblTitle.setStyleSheet("font-size:14px;padding-left:5px;")
        # 标题栏弹簧
        self.spacer = QSpacerItem(TITLE_SPACER_WIDTH, TITLE_BAR_HEIGHT, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 最小化按钮图标
        self.btnMin = QPushButton(self)
        # 最大化按钮图标
        self.btnMax = QPushButton(self)
        # 关闭按钮图标
        self.btnClose = QPushButton(self)
        # 窗体设置高度
        self.setFixedHeight(TITLE_BAR_HEIGHT)
        # 鼠标是否按下标识
        self.isPressed = False
        # 调用布局函数
        self.__f_layoutFunc()

    # 标题栏界面布局函数
    def __f_layoutFunc(self):
        """
        function:  标题栏界面布局函数
              in:  None
             out:  None
          return:  None
          others:  TitleBar Interface Layout Func
        """
        # 设置最小化按钮大小
        self.btnMin.setFixedSize(TITLE_BUTTON_WIDTH, TITLE_BUTTON_SIZE)
        # 设置最大化按钮大小
        self.btnMax.setFixedSize(TITLE_BUTTON_WIDTH, TITLE_BUTTON_SIZE)
        # 设置关闭按钮大小
        self.btnClose.setFixedSize(TITLE_BUTTON_WIDTH, TITLE_BUTTON_SIZE)
        # 设置按键背景色
        self.f_setBtnStyle(0)
        # 设置图标大小,设置标题高度
        self.lblIcon.setFixedSize(TITLE_LABEL_SIZE, TITLE_LABEL_SIZE)
        self.lblTitle.setFixedHeight(TITLE_LABEL_SIZE)
        # 图标及标题设置居中
        self.lblIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lblTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 设置最小化按钮背景
        self.btnMin.setIcon(QIcon(TITLE_MIN_ICON))
        # 设置最大化按钮背景
        self.btnMax.setIcon(QIcon(TITLE_MAX_ICON))
        # 设置关闭按钮背景
        self.btnClose.setIcon(QIcon(TITLE_CLS_ICON))
        # 最小化按钮关联事件
        self.btnMin.clicked.connect(self.__f_mininizedWindow)
        # 最大化按钮关联事件
        self.btnMax.clicked.connect(self.__f_maximizedWindow)
        # 关闭按钮关联事件
        self.btnClose.clicked.connect(self.__f_closeMainWindow)

        # 设置布局
        self.setLayout(self.layoutMain)

        # 设置控件间的距离
        self.layoutMain.setSpacing(0)
        self.layoutMain.setContentsMargins(0, 0, 0, 0)

        # 主布局添加控件
        self.layoutMain.addWidget(self.lblIcon)
        self.layoutMain.addWidget(self.lblTitle)
        self.layoutMain.addItem(self.spacer)
        self.layoutMain.addWidget(self.btnMin)
        self.layoutMain.addSpacerItem(QSpacerItem(5, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.layoutMain.addWidget(self.btnMax)
        self.layoutMain.addSpacerItem(QSpacerItem(5, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))
        self.layoutMain.addWidget(self.btnClose)
        self.layoutMain.addSpacerItem(QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed))

    # 设置窗体标题栏标题
    def f_setTitle(self, title):
        """
        function:  设置窗体标题栏标题
              in:  title：标题栏标题
             out:  None
          return:  None
          others:  Set Title Of The Form
        """
        # 设置标题
        self.lblTitle.setText(title)

    # 设置窗体图标
    def f_setIcon(self, icon):
        """
        function:  设置窗体图标
              in:  icon：icon图标的路径
             out:  None
          return:  None
          others:  Set Icon Of The Form
        """
        # 设置图标
        self.lblIcon.setPixmap(icon.scaled(self.lblIcon.size() - QSize(TITLE_ICON_MAG, TITLE_ICON_MAG)))

    # 窗体最小化
    def __f_mininizedWindow(self):
        """
        function:  窗体最小化
              in:  None
             out:  None
          return:  None
          others:  Form Minimization
        """
        # 窗体最小化
        self.parentForm.showMinimized()

    # 窗体最大化
    def __f_maximizedWindow(self):
        """
        function:  窗体最大化
              in:  None
             out:  None
          return:  None
          others:  Form Maximization
        """
        # 判断窗体是否最大化：如果是，维持原状；不过不是，最大化
        if self.parentForm.isMaximized():
            self.parentForm.showNormal()
            # 设置最大化按钮背景
            self.btnMax.setIcon(QIcon(TITLE_MAX_ICON))
        else:
            self.parentForm.showMaximized()
            # 设置最大化按钮背景
            self.btnMax.setIcon(QIcon(TITLE_RESTORE_ICON))

    # 窗体关闭
    def __f_closeMainWindow(self):
        """
        function:  窗体关闭
              in:  None
             out:  None
          return:  None
          others:  Form Closed
        """
        # 窗体关闭
        self.parentForm.close()

    # 窗体复原
    def __f_restoreWindow(self):
        """
        function:  窗体复原
              in:  None
             out:  None
          return:  None
          others:  Form Restored
        """
        # 判断窗体是否最大化：如果是，维持原状；不过不是，最大化
        if self.parentForm.isMaximized():
            self.parentForm.showNormal()
            # 设置最大化按钮背景
            self.btnMax.setIcon(QIcon(TITLE_MAX_ICON))
        else:
            self.parentForm.showMaximized()
            # 设置最大化按钮背景
            self.btnMax.setIcon(QIcon(TITLE_RESTORE_ICON))

    # 重写鼠标双击事件
    def mouseDoubleClickEvent(self, event):
        """
        function:  重写鼠标双击事件
              in:  None
             out:  None
          return:  QWidget().mouseDoubleClickEvent(event)
          others:  Override Double Clicked Event
        """
        # 调用窗体复原函数
        self.__f_restoreWindow()
        return QWidget().mouseDoubleClickEvent(event)

    # 重写鼠标按下事件
    def mousePressEvent(self, event):
        """
        function:  重写鼠标按下事件
              in:  None
             out:  None
          return:  QWidget().mousePressEvent(event)
          others:  Override Mouse Pressed Event
        """
        # 鼠标是否按下标识置为True
        self.isPressed = True
        # 获取鼠标按下位置坐标
        self.startPos = event.globalPos()
        return QWidget().mousePressEvent(event)

    # 重写鼠标释放事件
    def mouseReleaseEvent(self, event):
        """
        function:  重写鼠标释放事件
              in:  None
             out:  None
          return:  QWidget().mouseReleaseEvent(event)
          others:  Override Mouse Released Event
        """
        # 鼠标是否按下标识置为False
        self.isPressed = False
        return QWidget().mouseReleaseEvent(event)

    # 重写鼠标移动事件
    def mouseMoveEvent(self, event):
        """
        function:  重写鼠标移动事件
              in:  None
             out:  None
          return:  QWidget().mouseMoveEvent(event)
          others:  Override Mouse Moved Event
        """
        # 判断鼠标是否按下：如果鼠标按下并且窗口属于最大化，则保持现状
        if self.isPressed:
            if self.parentForm.isMaximized:
                self.parentForm.showNormal()
            # 获取鼠标位置
            movePos = event.globalPos() - self.startPos
            self.startPos = event.globalPos()
            # 窗体移动至鼠标现在的位置
            self.parentForm.move(self.parentForm.pos() + movePos)
        return QWidget().mouseMoveEvent(event)

    # 设置标题栏按键的背景色
    def f_setBtnStyle(self, themeIndex):
        """
        function:  设置标题栏按键的背景色
              in:  themeIndex：窗体的主题
                   0：dark
                   1：light
             out:  None
          return:  None
          others:  Set The Background Color Of The TitleBar Button
        """
        # dark主题
        if themeIndex == 0:
            self.btnMin.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_DARK, COLOR_DARK_HOVER))
            self.btnMax.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_DARK, COLOR_DARK_HOVER))
            self.btnClose.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_DARK, COLOR_DARK_HOVER))
        # light主题
        elif themeIndex == 1:
            self.btnMin.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_LIGHT, COLOR_LIGHT_HOVER))
            self.btnMax.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_LIGHT, COLOR_LIGHT_HOVER))
            self.btnClose.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_LIGHT, COLOR_LIGHT_HOVER))
        # 其他
        else:
            self.btnMin.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_DARK, COLOR_DARK_HOVER))
            self.btnMax.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_DARK, COLOR_DARK_HOVER))
            self.btnClose.setStyleSheet(
                "QPushButton {background: %s;} "
                "QPushButton:hover{background: %s;}" % (COLOR_DARK, COLOR_DARK_HOVER))
