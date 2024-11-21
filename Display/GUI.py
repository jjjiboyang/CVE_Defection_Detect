# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGraphicsView, QGridLayout,
    QLabel, QLayout, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)
import Display.icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1579, 867)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/title_icon/icon/\u8584\u819c\u7455\u75b5\u68c0\u6d4b.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionCameraGrab = QAction(MainWindow)
        self.actionCameraGrab.setObjectName(u"actionCameraGrab")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        sizePolicy1.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy1)
        self.widget_3.setMaximumSize(QSize(500, 16777215))
        self.widget_3.setStyleSheet(u"#widget_3{border:2px solid #31363B;border-radius:10px;}")
        self.gridLayout_4 = QGridLayout(self.widget_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.gridLayout_4.addLayout(self.verticalLayout_4, 1, 1, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_4.addLayout(self.verticalLayout_3, 1, 0, 1, 1)

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setMinimumSize(QSize(0, 30))
        self.label_4.setStyleSheet(u"font-size: 22px;font-weight: bold;color:#1DE9B6;")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 2)


        self.gridLayout_2.addWidget(self.widget_3, 1, 4, 1, 2)

        self.Start_Button = QPushButton(self.centralwidget)
        self.Start_Button.setObjectName(u"Start_Button")
        sizePolicy2.setHeightForWidth(self.Start_Button.sizePolicy().hasHeightForWidth())
        self.Start_Button.setSizePolicy(sizePolicy2)
        self.Start_Button.setMinimumSize(QSize(0, 80))
        self.Start_Button.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_2.addWidget(self.Start_Button, 3, 4, 1, 1)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setMaximumSize(QSize(500, 16777215))
        self.widget_2.setStyleSheet(u"#widget_2{border:2px solid #31363B;border-radius:10px;}\n"
"")
        self.gridLayout_3 = QGridLayout(self.widget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(0, 30))
        self.label.setStyleSheet(u"font-size: 22px;font-weight: bold;color:#1DE9B6;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout_3.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_3.addLayout(self.verticalLayout_2, 1, 0, 1, 1)


        self.gridLayout_2.addWidget(self.widget_2, 0, 4, 1, 2)

        self.Stop_Button = QPushButton(self.centralwidget)
        self.Stop_Button.setObjectName(u"Stop_Button")
        sizePolicy2.setHeightForWidth(self.Stop_Button.sizePolicy().hasHeightForWidth())
        self.Stop_Button.setSizePolicy(sizePolicy2)
        self.Stop_Button.setMinimumSize(QSize(0, 80))
        self.Stop_Button.setMaximumSize(QSize(250, 16777215))

        self.gridLayout_2.addWidget(self.Stop_Button, 3, 5, 1, 1)

        self.widget_1 = QWidget(self.centralwidget)
        self.widget_1.setObjectName(u"widget_1")
        sizePolicy1.setHeightForWidth(self.widget_1.sizePolicy().hasHeightForWidth())
        self.widget_1.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        self.widget_1.setFont(font)
        self.widget_1.setStyleSheet(u"#widget_1{border:2px solid #31363B;border-radius:10px;}\n"
"#label_1{border:2px solid #31363B;border-radius:5px;}\n"
"#label_2{border:2px solid #31363B;border-radius:5px;}\n"
"#label_3{border:2px solid #31363B;border-radius:5px;}\n"
"")
        self.gridLayout = QGridLayout(self.widget_1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.graphicsView_2 = QGraphicsView(self.widget_1)
        self.graphicsView_2.setObjectName(u"graphicsView_2")

        self.gridLayout_6.addWidget(self.graphicsView_2, 1, 1, 1, 1)

        self.graphicsView_1 = QGraphicsView(self.widget_1)
        self.graphicsView_1.setObjectName(u"graphicsView_1")

        self.gridLayout_6.addWidget(self.graphicsView_1, 1, 0, 1, 1)

        self.label_3 = QLabel(self.widget_1)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setPointSize(15)
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout_6.addWidget(self.label_3, 0, 2, 1, 1)

        self.label_1 = QLabel(self.widget_1)
        self.label_1.setObjectName(u"label_1")
        sizePolicy1.setHeightForWidth(self.label_1.sizePolicy().hasHeightForWidth())
        self.label_1.setSizePolicy(sizePolicy1)
        self.label_1.setMinimumSize(QSize(0, 0))
        self.label_1.setMaximumSize(QSize(16777215, 40))
        self.label_1.setFont(font1)
        self.label_1.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout_6.addWidget(self.label_1, 0, 0, 1, 1)

        self.graphicsView_3 = QGraphicsView(self.widget_1)
        self.graphicsView_3.setObjectName(u"graphicsView_3")

        self.gridLayout_6.addWidget(self.graphicsView_3, 1, 2, 1, 1)

        self.label_2 = QLabel(self.widget_1)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 40))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout_6.addWidget(self.label_2, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_6, 1, 0, 1, 3)


        self.gridLayout_2.addWidget(self.widget_1, 0, 1, 4, 1)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)
        self.widget.setMinimumSize(QSize(0, 0))
        self.widget.setStyleSheet(u"#widget{border:2px solid #31363B;border-radius:10px;}")
        self.verticalLayout_7 = QVBoxLayout(self.widget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy4)
        self.label_13.setMinimumSize(QSize(0, 30))
        self.label_13.setStyleSheet(u"font-size: 22px;font-weight: bold;color:#1DE9B6;")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_13)

        self.listWidget = QListWidget(self.widget)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy5)
        self.listWidget.setMinimumSize(QSize(0, 0))
        self.listWidget.setFont(font1)
        self.listWidget.setStyleSheet(u"")
        self.listWidget.setSortingEnabled(False)

        self.verticalLayout_7.addWidget(self.listWidget)

        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy3.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy3)
        self.label_12.setMaximumSize(QSize(16777215, 500))
        self.label_12.setStyleSheet(u"background:#49545A;\n"
"font-size:17px;")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_12)


        self.gridLayout_2.addWidget(self.widget, 0, 3, 4, 1)

        self.widget_4 = QWidget(self.centralwidget)
        self.widget_4.setObjectName(u"widget_4")
        sizePolicy2.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy2)
        self.widget_4.setMaximumSize(QSize(500, 16777215))
        self.widget_4.setStyleSheet(u"#widget_4{border:2px solid #31363B;border-radius:10px;}")
        self.gridLayout_8 = QGridLayout(self.widget_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_5.setHorizontalSpacing(0)
        self.gridLayout_5.setVerticalSpacing(4)
        self.gridLayout_5.setContentsMargins(-1, 10, -1, 10)
        self.checkBox_1 = QCheckBox(self.widget_4)
        self.checkBox_1.setObjectName(u"checkBox_1")
        self.checkBox_1.setChecked(True)
        self.checkBox_1.setAutoExclusive(False)

        self.gridLayout_5.addWidget(self.checkBox_1, 5, 2, 1, 1)

        self.label_7 = QLabel(self.widget_4)
        self.label_7.setObjectName(u"label_7")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy6)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_7, 5, 0, 1, 1)

        self.label_5 = QLabel(self.widget_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy6.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy6)
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)

        self.checkBox_5 = QCheckBox(self.widget_4)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_5, 2, 1, 1, 1)

        self.checkBox_4 = QCheckBox(self.widget_4)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_4, 0, 2, 1, 1)

        self.label_6 = QLabel(self.widget_4)
        self.label_6.setObjectName(u"label_6")
        sizePolicy6.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy6)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_5.addWidget(self.label_6, 2, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.widget_4)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout_5.addWidget(self.checkBox_3, 0, 1, 1, 1)

        self.checkBox_2 = QCheckBox(self.widget_4)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_2, 5, 1, 1, 1)

        self.checkBox_9 = QCheckBox(self.widget_4)
        self.checkBox_9.setObjectName(u"checkBox_9")
        self.checkBox_9.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_9, 6, 1, 1, 1)

        self.checkBox_10 = QCheckBox(self.widget_4)
        self.checkBox_10.setObjectName(u"checkBox_10")
        self.checkBox_10.setChecked(True)

        self.gridLayout_5.addWidget(self.checkBox_10, 6, 2, 1, 1)

        self.checkBox_6 = QCheckBox(self.widget_4)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.gridLayout_5.addWidget(self.checkBox_6, 2, 2, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_5, 0, 0, 1, 2)


        self.gridLayout_2.addWidget(self.widget_4, 2, 4, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.widget_2.raise_()
        self.widget_1.raise_()
        self.widget_3.raise_()
        self.Start_Button.raise_()
        self.Stop_Button.raise_()
        self.widget_4.raise_()
        self.widget.raise_()
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1579, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menu.addSeparator()

        self.retranslateUi(MainWindow)

        self.listWidget.setCurrentRow(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u533b\u7528\u900f\u660e\u7ba1\u6750\u673a\u5668\u89c6\u89c9\u5728\u7ebf\u68c0\u6d4b\u7cfb\u7edf", None))
        self.actionCameraGrab.setText(QCoreApplication.translate("MainWindow", u"CameraGrab", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u7cfb\u7edf\u4fe1\u606f", None))
        self.Start_Button.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u68c0\u6d4b", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u751f\u4ea7\u4fe1\u606f", None))
        self.Stop_Button.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u68c0\u6d4b", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u7f3a\u9677\u56fe\u50cf\u6d4f\u89c8", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u673a1\u5b9e\u65f6\u56fe\u50cf", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u673a2\u5b9e\u65f6\u56fe\u50cf", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5e93", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u7f3a\u9677\u56fe\u7247", None))
        self.checkBox_1.setText(QCoreApplication.translate("MainWindow", u"\u6676\u5706\u6c34\u6591\u7f3a\u9677", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u62a5\u8b66\u9009\u9879\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u56fe\u50cf\uff1a", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"\u666e\u901a\u5439\u6c14 ", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"\u7f3a\u9677\u56fe\u50cf", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5439\u6c14\u9009\u9879\uff1a", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"\u6240\u6709\u56fe\u50cf", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u957f\u6761\u5212\u75d5\u7f3a\u9677", None))
        self.checkBox_9.setText(QCoreApplication.translate("MainWindow", u"\u7cca\u6599\u9ed1\u70b9\u7f3a\u9677", None))
        self.checkBox_10.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u7eed\u6676\u5706\u7f3a\u9677", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"\u77ed\u7ba1\u53cd\u5411\u5439\u6c14", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u63a7\u5236", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
    # retranslateUi

