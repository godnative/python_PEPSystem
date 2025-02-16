from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, \
    QAbstractItemView, QHeaderView, QCheckBox, QTableWidgetItem
from qfluentwidgets import PushButton, SearchLineEdit, TableWidget, LineEdit, CalendarPicker, ComboBox, MessageBoxBase, \
    SubtitleLabel

from utils.utils_tool import get_datestr_from_timestamp


class BaseMessageBoxWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
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
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        layout = QHBoxLayout()  # 这里直接将 QVBoxLayout 设置为 self 的布局

        self.addButton = PushButton("add")

        self.searchInput = SearchLineEdit(self)
        self.searchInput.setPlaceholderText('Search')
        self.searchInput.setFixedWidth(500)

        self.delButton = PushButton("del")

        self.ModButton = PushButton("Mod")

        layout.addWidget(self.addButton)
        layout.addWidget(self.searchInput)
        layout.addWidget(self.delButton)
        layout.addWidget(self.ModButton)

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
        for row, data in enumerate(datas):
            # checkBox = QCheckBox()
            # self.tableWidget.setCellWidget(row, 0, checkBox)
            for column, key in enumerate(header_info):
                if key == "student_gender":
                    value = "男" if data.get(key, "") == 0 else "女"
                else:
                    value = data.get(key, "")
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row, column, item)


class BaseMainInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        title_info_box = QHBoxLayout()
        self.label = QLabel(self)
        title_info_box.addWidget(self.label)

        self.label_2 = QLabel()
        title_info_box.addWidget(self.label_2)

        vbox.addLayout(title_info_box)
        self.BaseQuery = BaseQueryWidget(self)
        vbox.addWidget(self.BaseQuery)