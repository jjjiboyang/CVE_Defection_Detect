import multiprocessing
import time
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSizePolicy, QButtonGroup, QSpacerItem
from Display.GUI import Ui_MainWindow
from Display.GraphicsView_One import CustomGraphicsView
from Display.GraphicsView_Two import ImageListView
from Display.Menu_Action import MenuAction
from Display.ProductInfoLeft import ProductInfoWidgetLeft
from Display.ProductInfoRight import ProductInfoWidgetRight
from Display.StatusInfoLeft import StatusInfoWidgetLeft
from Display.StatusInfoRight import StatusInfoWidgetRight
from Display.sub_rec_image import EcalReceiverThread
from Display.WindowTitle import ctQTitleBar
from Display.StatusBar import StatusBar
from Display.PushButton import PushButton
from Log.logger import LoggerManager
from Display.CheckBox import CheckBox
from multiprocessing import Process
from EncoderIO.SignalGrab import run_SignalGrab
from Algorithm.ProcessImage import run_ImageProcessing
from Display.database_list import ImageDisplayWidget
from Algorithm.SaveImage import SaveImage_ecal
from Algorithm.blow_logic import blow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 日志
        self.logger = LoggerManager.get_logger()
        self.message_queue = multiprocessing.Queue()
        self.light_queue = multiprocessing.Queue()
        self.blow_queue = multiprocessing.Queue()
        self.image_encoder_queue = multiprocessing.Queue()
        self.defect_types=[0,1,1,1]

        # 启动发送编码器和IO信号的进程
        self.light_queue.put("ready")
        try:
            self.process_signal = Process(target=run_SignalGrab)
            self.process_signal.start()
        except Exception as e:
            self.logger.error(e)

        # 初始化
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.status = False
        self.save_choice = 1

        '''隐藏系统标题栏并且自己设置'''
        # 创建标题栏
        self.title = ctQTitleBar(self)
        # 设置标题栏图标
        self.title.f_setIcon(QPixmap(":title_icon/icon/薄膜瑕疵检测.png"))
        # 隐藏主窗口边框
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 新建布局
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # 去除边距
        self.mainLayout.setSpacing(0)  # 去除控件间距
        # 将标题栏添加到主布局中
        self.mainLayout.addWidget(self.title)
        # 现有的布局
        self.existingLayout = QVBoxLayout()
        self.existingLayout.addWidget(self.ui.menubar)
        self.ui.menubar.setStyleSheet("background-color:#232629;")
        self.existingLayout.addWidget(self.ui.centralwidget)
        self.ui.centralwidget.setStyleSheet("background-color: #4F5B62;")
        # 创建一个新的中央小部件，并设置布局
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #232629;")
        central_widget.setLayout(self.mainLayout)
        central_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setCentralWidget(central_widget)
        # 添加现有布局到新的中央小部件
        self.mainLayout.addLayout(self.existingLayout)
        self.ui.menubar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        '''设置Menu和Action'''
        self.menu_action = MenuAction(self.ui,self.logger)

        '''字体大小'''
        self.ui.label_1.setStyleSheet("font-size: 20px;font-weight: bold;color:White;")
        self.ui.label_2.setStyleSheet("font-size: 20px;font-weight: bold;color:White;")
        self.ui.label_3.setStyleSheet("font-size: 20px;font-weight: bold;color:White;")
        self.ui.Start_Button.setStyleSheet("font-size: 20px;font-weight: bold;")
        self.ui.Stop_Button.setStyleSheet("font-size: 20px;font-weight: bold;")

        '''第一个GraphicView'''
        self.ui.graphicsView_1.deleteLater()
        self.ui.graphicsView_1 = CustomGraphicsView(self.ui.widget_1)
        self.ui.graphicsView_1.setObjectName(u"graphicsView_1")
        # 添加布局
        self.ui.gridLayout_6.addWidget(self.ui.graphicsView_1, 1, 0, 1, 1)

        '''第二个GraphicView'''
        self.ui.graphicsView_2.deleteLater()
        self.ui.graphicsView_2 = CustomGraphicsView(self.ui.widget_1)
        self.ui.graphicsView_2.setObjectName(u"graphicsView_2")
        # 添加布局
        self.ui.gridLayout_6.addWidget(self.ui.graphicsView_2, 1, 1, 1, 1)

        '''第三个GraphicView'''
        # 获取当前日期并格式化
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.ui.graphicsView_3.deleteLater()
        self.ui.graphicsView_3 = ImageListView(f"./All_Images/{current_date}/defect_images/", self.ui.widget_1)
        self.ui.graphicsView_3.setObjectName(u"graphicsView_3")
        self.ui.graphicsView_3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 添加布局
        self.ui.gridLayout_6.addWidget(self.ui.graphicsView_3, 1, 2, 1, 1)

        '''生产信息'''
        self.product_info_widget_1 = ProductInfoWidgetLeft(self.ui.graphicsView_3)
        self.product_info_widget_2 = ProductInfoWidgetRight(self.ui.graphicsView_3)
        self.ui.verticalLayout_2.addWidget(self.product_info_widget_1)
        self.ui.verticalLayout.addWidget(self.product_info_widget_2)

        '''运行状态'''
        self.status_widget_1 = StatusInfoWidgetLeft()
        self.status_widget_2 = StatusInfoWidgetRight()
        self.ui.verticalLayout_3.addWidget(self.status_widget_1)
        self.ui.verticalLayout_4.addWidget(self.status_widget_2)

        '''绑定按钮和设置按钮样式'''
        self.PushButtonOperator = PushButton(self.ui)
        self.ui.Start_Button.pressed.connect(self.PushButtonOperator.HideText)
        self.ui.Start_Button.released.connect(self.PushButtonOperator.ShowText)
        self.ui.Start_Button.setStyleSheet("font-size:20px;background-color: #232629;")
        self.ui.Stop_Button.setStyleSheet("font-size:20px;background-color: #232629;")
        self.ui.Stop_Button.setEnabled(False)
        self.ui.Start_Button.clicked.connect(self.status_widget_1.start_timing)
        self.ui.Stop_Button.clicked.connect(self.status_widget_1.stop_timing)
        self.ui.Start_Button.clicked.connect(self.start_button_clicked)
        self.ui.Stop_Button.clicked.connect(self.stop_button_clicked)

        '''展示'''
        self.ecal_receiver_thread = EcalReceiverThread()
        self.ecal_receiver_thread.image_received_1.connect(self.update_graphics_view_1)
        self.ecal_receiver_thread.image_received_2.connect(self.update_graphics_view_2)
        self.ecal_receiver_thread.start()

        '''CheckBox'''
        self.cBox = CheckBox(self.ui, self.light_queue,self.blow_queue)
        self.ui.checkBox_5.stateChanged.connect(self.cBox.on_checkbox5_changed)
        self.ui.checkBox_6.stateChanged.connect(self.cBox.on_checkbox6_changed)
        self.ui.checkBox_4.stateChanged.connect(self.save_image_choice)
        self.ui.checkBox_1.stateChanged.connect(self.defect_type_change)
        self.ui.checkBox_2.stateChanged.connect(self.defect_type_change)
        self.ui.checkBox_9.stateChanged.connect(self.defect_type_change)
        self.ui.checkBox_10.stateChanged.connect(self.defect_type_change)

        '''StatusBar'''
        self.status_text = StatusBar(self.ui)

        '''数据库'''
        self.image_display_widget = ImageDisplayWidget(self.ui, self.message_queue)
        self.ui.listWidget.setStyleSheet("""
            QListWidget::item {
                border-bottom: 2px solid #31363B;  /* 设置分割线 */
            }

            QListWidget {
                font-size: 15px;  /* 设置字体大小 */
                font-family: Arial;  /* 设置字体类型 */}
        """)

    def defect_type_change(self):
        if self.ui.checkBox_2.isChecked():
            self.defect_types[0] = 1
        else:
            self.defect_types[0] = 0
        if self.ui.checkBox_1.isChecked():
            self.defect_types[1] = 1
        else:
            self.defect_types[1] = 0
        if self.ui.checkBox_9.isChecked():
            self.defect_types[2] = 1
        else:
            self.defect_types[2] = 0
        if self.ui.checkBox_10.isChecked():
            self.defect_types[3] = 1
        else:
            self.defect_types[3] = 0
        print(self.defect_types)

    def save_image_choice(self):
        if self.ui.checkBox_4.isChecked():
            self.save_choice = 1
        else:
            self.save_choice = 0

    def start_button_clicked(self):
        if not self.status:
            # 设置按钮样式
            self.ui.Start_Button.setEnabled(False)
            self.ui.Stop_Button.setEnabled(True)
            self.ecal_receiver_thread.start_receive()
            self.process_image = Process(target=run_ImageProcessing,
                                         args=(self.save_choice, self.image_encoder_queue,self.defect_types))
            self.process_image.start()
            self.save_image = Process(target=SaveImage_ecal, args=(self.save_choice, self.message_queue))
            self.save_image.start()
            self.blow_logic = Process(target=blow, args=(self.image_encoder_queue,self.blow_queue))
            self.blow_logic.start()
            self.status = True
            self.light_queue.put("run")
            self.status_text.show("开始接收图片")
            self.logger.info("开始接收图片")

    def update_graphics_view_1(self, img):
        self.ui.graphicsView_1.set_image(img)
        self.status_widget_2.update_1()

    def update_graphics_view_2(self, img):
        self.ui.graphicsView_2.set_image(img)
        self.status_widget_2.update_2()

    def stop_button_clicked(self):
        if self.status:
            # 设置按钮样式
            self.ui.Start_Button.setEnabled(True)
            self.ui.Stop_Button.setEnabled(False)

            self.ecal_receiver_thread.stop_receive()
            self.process_image.terminate()
            self.save_image.terminate()
            self.blow_logic.terminate()
            self.status = False
            self.light_queue.put("stop")
            self.status_text.show("停止接收图片")
            self.logger.info("停止接收图片")

    def closeEvent(self, event):
        self.light_queue.put("close")
        self.status_widget_2.close_window()
        self.stop_button_clicked()
        self.ecal_receiver_thread.terminate()
        self.process_signal.terminate()
        # 关闭信号接发的进程
        self.cBox.blow_signal.terminate()
        # 关闭采集图像的进程
        self.ui.actionClose_Camera.trigger()
        self.logger.info("关闭窗口")
        event.accept()  # 接受关闭事件
        QApplication.quit()  # 结束主事件循环并退出程序

        # 额外的检查：确保所有线程都被终止
        # for thread in threading.enumerate():
        #     if thread is not threading.main_thread():
        #         self.logger.info(f"Joining thread: {thread.name}")
        #         thread.join(timeout=1)
