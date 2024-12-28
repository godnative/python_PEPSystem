from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, QDate
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QLineEdit
from qfluentwidgets import CalendarPicker, TextEdit

from utils.utils_tool import ImageLabel, qdate_to_timestamp, timestamp_to_date


class BaseSchoolInterface_Temp:
    def __init__(self):
        self.BaseSchoolInterface_layout = QVBoxLayout()

        self.horizontalLayout = QHBoxLayout()
        self.label = ImageLabel()
        self.label_title = QLabel()

        self.verticalLayout = QVBoxLayout()
        self.label_2 = QLabel()
        self.lineEdit_2 = QLineEdit()
        self.label_3 = QLabel()

        self.calendarPicker = CalendarPicker()
        # 设置当前日期
        self.calendarPicker.setDate(QDate(2024, 2, 26))

        self.lineEdit_3 = QLineEdit()
        self.label_4 = QLabel()
        self.lineEdit_4 = QLineEdit()
        self.textEdit = TextEdit()

        self.setup_ui()
        # TODO:学校图像修改

    def setup_ui(self):
        self.label.setMinimumSize(QSize(400, 400))
        self.label.setMaximumSize(QSize(500, 500))
        # self.label.setText("")
        # self.label.setPixmap(QPixmap("./login/resource/images/background.jpg"))
        self.label.setScaledContents(True)
        self.horizontalLayout.addWidget(self.label)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        font = QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        self.label_title.setFont(font)
        self.label_title.setText("")

        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setFont(font)
        self.label_2.setText("教区名字")

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_2.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.lineEdit_2)

        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setFont(font)
        self.label_3.setText("建立日期")
        self.verticalLayout.addWidget(self.label_3)

        self.calendarPicker.setMinimumSize(QSize(0, 40))
        # self.lineEdit_3.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.calendarPicker)

        self.label_4.setMaximumSize(QSize(16777215, 20))
        self.label_4.setFont(font)
        self.label_4.setText("地址")
        self.verticalLayout.addWidget(self.label_4)

        self.lineEdit_4.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.lineEdit_4)

        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.BaseSchoolInterface_layout.addWidget(self.label_title)
        self.BaseSchoolInterface_layout.addLayout(self.horizontalLayout)
        self.BaseSchoolInterface_layout.addWidget(self.textEdit)

    def get_InputSchoolDialoginfo(self):
        # 获取输入框中的数据并返回
        school_info = {
            'school_name': self.lineEdit_2.text(),
            'school_address': self.lineEdit_4.text(),
            'school_info': self.textEdit.toPlainText(),
            'school_date': qdate_to_timestamp(self.calendarPicker.date)
        }
        return school_info

    def set_school_info(self, school_info):
        # 设置学生信息
        self.lineEdit_2.setText(school_info['school_name'])
        self.lineEdit_4.setText(school_info['school_address'])
        self.textEdit.setText(school_info['school_info'])
        qDate = timestamp_to_date(school_info["school_date"])
        # 设置文本框的文本为格式化后的日期时间
        self.calendarPicker.setDate(qDate)
