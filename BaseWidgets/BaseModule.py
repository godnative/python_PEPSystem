from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, \
    QAbstractItemView, QHeaderView, QTableWidgetItem, QApplication, QGridLayout, QCheckBox
from qfluentwidgets import PushButton, SearchLineEdit, TableWidget, LineEdit, CalendarPicker, ComboBox, CheckBox

from utils.utils_tool import get_now_date, timestamp_to_date, timestamp_to_times

user_type = ["管理员", "录入员", "游客"]
opera_type = ["录入", "待审阅", "归档"]


class BaseMessageBoxWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        hbox = QHBoxLayout(self)
        self.pic = QLabel("inc pic")
        hbox.addWidget(self.pic)

        vbox = QVBoxLayout()

        hbox_1 = QHBoxLayout()
        self.label_1 = QLabel("label_1")
        self.inputLine_1 = LineEdit()
        self.label_2 = QLabel("label_2")
        self.inputLine_2 = LineEdit()
        hbox_1.addWidget(self.label_1)
        hbox_1.addWidget(self.inputLine_1)
        hbox_1.addWidget(self.label_2)
        hbox_1.addWidget(self.inputLine_2)
        vbox.addLayout(hbox_1)

        hbox_2 = QHBoxLayout()
        self.label_3 = QLabel("label_3")
        self.inputLine_3 = LineEdit()
        self.label_4 = QLabel("label_4")
        self.inputLine_4 = LineEdit()
        hbox_2.addWidget(self.label_3)
        hbox_2.addWidget(self.inputLine_3)
        hbox_2.addWidget(self.label_4)
        hbox_2.addWidget(self.inputLine_4)
        vbox.addLayout(hbox_2)

        hbox_3 = QHBoxLayout()
        self.label_5 = QLabel("label_5")
        self.inputLine_5 = LineEdit()
        self.label_6 = QLabel("label_6")
        self.inputLine_6 = LineEdit()
        hbox_3.addWidget(self.label_5)
        hbox_3.addWidget(self.inputLine_5)
        hbox_3.addWidget(self.label_6)
        hbox_3.addWidget(self.inputLine_6)
        vbox.addLayout(hbox_3)

        hbox_4 = QHBoxLayout()
        self.label_7 = QLabel("label_7")
        self.inputLine_7 = LineEdit()
        self.label_8 = QLabel("label_8")
        self.inputLine_8 = LineEdit()
        hbox_4.addWidget(self.label_7)
        hbox_4.addWidget(self.inputLine_7)
        hbox_4.addWidget(self.label_8)
        hbox_4.addWidget(self.inputLine_8)
        vbox.addLayout(hbox_4)

        hbox_5 = QHBoxLayout()
        self.label_9 = QLabel("label_9")
        self.inputLine_9 = ComboBox()
        self.label_10 = QLabel("label_10")
        self.inputLine_10 = CalendarPicker()
        self.inputLine_10.setDate(get_now_date())
        hbox_5.addWidget(self.label_9)
        hbox_5.addWidget(self.inputLine_9)
        hbox_5.addWidget(self.label_10)
        hbox_5.addWidget(self.inputLine_10)
        vbox.addLayout(hbox_5)

        hbox_6 = QHBoxLayout()
        self.label_11 = QLabel("label_11")
        self.inputLine_11 = ComboBox()
        self.label_12 = QLabel("label_12")
        self.inputLine_12 = PushButton()
        hbox_6.addWidget(self.label_11)
        hbox_6.addWidget(self.inputLine_11)
        hbox_6.addWidget(self.label_12)
        hbox_6.addWidget(self.inputLine_12)
        vbox.addLayout(hbox_6)

        hbox_7 = QHBoxLayout()
        self.label_13 = QLabel("label_13")
        self.inputLine_13 = LineEdit()
        hbox_7.addWidget(self.label_13)
        hbox_7.addWidget(self.inputLine_13)
        vbox.addLayout(hbox_7)

        hbox.addLayout(vbox)


class BaseQueryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        vbox = QVBoxLayout(self)
        layout = QHBoxLayout()  # 这里直接将 QVBoxLayout 设置为 self 的布局

        self.addButton = PushButton()
        self.addButton.setText("添加")

        self.searchInput = SearchLineEdit(self)
        self.searchInput.setPlaceholderText('Search')
        self.searchInput.setFixedWidth(500)

        self.delButton = PushButton()
        self.delButton.setText("删除")

        self.ModButton = PushButton()
        self.ModButton.setText("修改")

        self.ReviewButton = PushButton()
        self.ReviewButton.setText("归档")
        # self.ReviewButton.hide()

        self.printButton = PushButton()
        self.printButton.setText("打印")
        self.printButton.hide()

        layout.addWidget(self.addButton)
        layout.addWidget(self.searchInput)
        layout.addWidget(self.delButton)
        layout.addWidget(self.ModButton)
        layout.addWidget(self.ReviewButton)
        layout.addWidget(self.printButton)

        self.tableWidget = TableWidget(self)
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        vbox.addLayout(layout)
        vbox.addWidget(self.tableWidget)

    def set_viewWidget_data(self, header_info, datas):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(datas))
        if self.tableWidget.horizontalHeaderItem(len(header_info)).text() == "归档":
            user_type_table = 0
        else:
            user_type_table = 1
        for row, data in enumerate(datas):
            review_filed_checkBox = QCheckBox()
            self.tableWidget.setCellWidget(row, len(header_info), review_filed_checkBox)
            for column, key in enumerate(header_info):
                if key == "student_gender":
                    value = "男" if data.get(key, "") == 0 else "女"
                elif key == "student_birthday" or key == "holyevent_date":
                    value = timestamp_to_date(data.get(key, "")).toString("yyyy-MM-dd")
                elif key == "opera_time":
                    value = timestamp_to_times(data.get(key, ""))
                elif key == "opera_type":
                    value = data.get(key, "")
                    if user_type_table == 0 and value != 1:
                        review_filed_checkBox.setDisabled(True)
                    elif user_type_table == 1 and value != 0:
                        review_filed_checkBox.setDisabled(True)
                    value = opera_type[data.get(key, "")]
                else:
                    value = data.get(key, "")
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, column, item)


class BaseMainInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        vbox = QVBoxLayout(self)
        title_info_box = QHBoxLayout()
        self.label = QLabel(self)
        title_info_box.addWidget(self.label)

        self.label_2 = QLabel()
        title_info_box.addWidget(self.label_2)

        vbox.addLayout(title_info_box)
        self.BaseQuery = BaseQueryWidget(self)
        vbox.addWidget(self.BaseQuery)


class BaseUserInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkBox_maxtir = None
        self.user_type = ["管理员", "录入员", "游客"]

        vbox = QVBoxLayout(self)
        title_info_box = QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(100, 20)
        self.label = QLabel(self)
        title_info_box.addWidget(self.label)
        title_info_box.addItem(spacerItem)

        user_info_box = QGridLayout()
        self.label_name = QLabel("姓名")
        user_info_box.addWidget(self.label_name, 0, 0)
        self.line_name = LineEdit(self)
        # self.line_name.setMaximumWidth(200)
        user_info_box.addWidget(self.line_name, 0, 1)
        self.label_type = QLabel("人员类别")
        user_info_box.addWidget(self.label_type, 1, 0)
        self.line_type = ComboBox(self)
        self.line_type.addItems(user_type)
        # self.line_type.setMaximumWidth(200)
        user_info_box.addWidget(self.line_type, 1, 1)
        self.label_note = QLabel("备注")
        user_info_box.addWidget(self.label_note, 2, 0)
        self.line_note = LineEdit(self)
        # self.line_note.setMaximumWidth(200)
        user_info_box.addWidget(self.line_note, 2, 1)

        self.label_password = QLabel("密码")
        user_info_box.addWidget(self.label_password, 3, 0)
        self.line_password = LineEdit(self)
        # self.line_note.setMaximumWidth(200)
        user_info_box.addWidget(self.line_password, 3, 1)

        title_info_box.addLayout(user_info_box)

        title_info_box.addItem(spacerItem)

        user_authiory_box = QGridLayout()
        permission_operation = ['', '添加', '删除', '修改']
        modules = ['', '人员', '家庭', '事件', '教区', '权限']
        for i, module in enumerate(permission_operation):
            label = QLabel(module)
            user_authiory_box.addWidget(label, 0, i)

        for i, module in enumerate(modules):
            label = QLabel(module)
            user_authiory_box.addWidget(label, i, 0)

        self.checkBox_maxtir = []

        for i in range(1, len(modules)):
            for j in range(1, len(permission_operation)):
                checkBox = CheckBox()
                self.checkBox_maxtir.append(checkBox)
                user_authiory_box.addWidget(checkBox, i, j)

        title_info_box.addLayout(user_authiory_box)
        vbox.addLayout(title_info_box)

        self.BaseQuery = BaseQueryWidget(self)
        self.BaseQuery.delButton.hide()
        self.BaseQuery.addButton.hide()
        self.BaseQuery.searchInput.hide()
        self.BaseQuery.ModButton.hide()
        vbox.addWidget(self.BaseQuery)

        self.line_type.currentIndexChanged.connect(self.change_set_checkbox)

    def set_checkbox_state_from_bitmap(self, bitmap):
        """
        根据输入的 bitmap 来设置 checkbox 的状态
        :param bitmap: 一个整数，每一位控制一个 checkbox 的状态
        """
        for i, checkbox in enumerate(self.checkBox_maxtir):
            # 检查 bitmap 的第 i 位是否为 1
            bit = (bitmap >> i) & 1
            checkbox.setChecked(bit == 1)

    def get_bitmap_from_checkbox_state(self):
        """
        根据 checkbox 的状态生成一个 bitmap 数
        :return: 一个整数，每一位代表一个 checkbox 的状态
        """
        bitmap = 0
        for i, checkbox in enumerate(self.checkBox_maxtir):
            if checkbox.isChecked():
                bitmap |= (1 << i)
        return bitmap

    def set_all_checkbox_state(self, state):
        """
        根据输入的 state 来设置所有 checkbox 的状态
        :param state: 一个布尔值，控制所有 checkbox 的状态
        """
        for checkbox in self.checkBox_maxtir:
            checkbox.setEnabled(state)

    def set_user_info(self, user_info):
        self.line_name.setText(user_info["user_name"])
        self.line_type.setCurrentIndex(user_info["user_type"])
        self.line_note.setText(user_info["user_note"])
        self.set_checkbox_state_from_bitmap(user_info["user_authnum"])

    def change_set_checkbox(self):
        if self.line_type.currentIndex() == 0:
            self.set_checkbox_state_from_bitmap(32767)
        elif self.line_type.currentIndex() == 1:
            self.set_checkbox_state_from_bitmap(4681)
        else:
            self.set_checkbox_state_from_bitmap(0)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    main_window = BaseUserInterface()
    main_window.show()

    sys.exit(app.exec())
