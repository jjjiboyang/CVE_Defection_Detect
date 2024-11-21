from PySide6.QtWidgets import QLabel, QVBoxLayout, QLineEdit, QWidget
from PySide6.QtCore import Qt
import sys

sys.path.append('data_json.py')
from Display.data_json import save_to_file
from Display.data_json import load_from_file


class ProductInfoWidgetLeft(QWidget):
    def __init__(self, graphics_view):
        super().__init__()

        data = load_from_file()
        if "产品名称" in data:
            self.ProductName = data["产品名称"]
        else:
            self.ProductName = "产品名称: 请输入产品名称"
        if "客户名称" in data:
            self.ClientName = data["客户名称"]
        else:
            self.ClientName = "客户名称: 请输入客户名称"
        if "订单编号" in data:
            self.OrderNumber = data["订单编号"]
        else:
            self.OrderNumber = "订单编号: 请输入订单编号"
        if "产品总数" in data:
            self.ProductNumber = data["产品总数"]
        else:
            self.ProductNumber = "产品总数: 请输入产品总数"
        if "机器编号" in data:
            self.MachineNumber = data["机器编号"]
        else:
            self.MachineNumber = "机器编号: 请输入机器编号"
        if "操作人员" in data:
            self.OperatorName = data["操作人员"]
        else:
            self.OperatorName = "操作人员: 请输入操作人名称"

        # 创建各个标签
        self.client_name_label = NameLabel(f"{self.ClientName}", min_height=30)
        self.product_name_label = NameLabel(f"{self.ProductName}", min_height=30)
        self.order_number_label = NameLabel(f"{self.OrderNumber}", min_height=30)
        self.product_number_label = NameLabel(f"{self.ProductNumber}", min_height=30)
        self.machine_number_label = NameLabel(f"{self.MachineNumber}", min_height=30)
        self.operator_name_label = NameLabel(f"{self.OperatorName}", min_height=30)

        self.client_name_label.setStyleSheet("font-size:17px;")
        self.product_name_label.setStyleSheet("font-size:17px;")
        self.order_number_label.setStyleSheet("font-size:17px;")
        self.product_number_label.setStyleSheet("font-size:17px;")
        self.machine_number_label.setStyleSheet("font-size:17px;")
        self.operator_name_label.setStyleSheet("font-size:17px;")

        # 设置其他标签的最小尺寸和对齐方式
        labels = [

        ]
        for label in labels:
            label.setMinimumSize(0, 30)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 创建垂直布局并添加标签
        layout = QVBoxLayout(self)
        layout.addWidget(self.client_name_label)
        layout.addWidget(self.product_name_label)
        layout.addWidget(self.order_number_label)
        layout.addWidget(self.product_number_label)
        layout.addWidget(self.machine_number_label)
        layout.addWidget(self.operator_name_label)


class NameLabel(QWidget):
    def __init__(self, text, min_width=150, min_height=30):
        super().__init__()
        self.label = QLabel(text)
        self.line_edit = QLineEdit(text)
        self.line_edit.hide()

        # 设置 QLabel 和 QLineEdit 的最小尺寸
        self.label.setMinimumSize(min_width, min_height)
        self.line_edit.setMinimumSize(min_width, min_height)

        # 设置标签和编辑框的对齐方式
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.line_edit.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # 使用水平布局管理标签和编辑框
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)

        # 设置布局中的标签间距
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 双击启用编辑
        self.label.mouseDoubleClickEvent = self.enable_editing
        self.line_edit.editingFinished.connect(self.finish_editing)

    def enable_editing(self, event):
        self.label.hide()
        self.line_edit.show()
        self.line_edit.setFocus()

    def finish_editing(self):
        self.label.setText(self.line_edit.text())
        save_to_file({(self.line_edit.text())[0:4]: self.line_edit.text()})
        self.line_edit.hide()
        self.label.show()
