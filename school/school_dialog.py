import os

from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, QDate, Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from qfluentwidgets import CalendarPicker, LineEdit

from utils.utils_tool import ImageLabel, qdate_to_timestamp, timestamp_to_date


class BaseSchoolInterface_Temp:
    def __init__(self):
        self.BaseSchoolInterface_layout = QVBoxLayout()

        self.horizontalLayout = QHBoxLayout()
        self.label = ImageLabel()
        self.label.setMinimumSize(QSize(400, 400))
        self.label.setMaximumSize(QSize(500, 500))
        # self.label.setText("")
        # self.label.setPixmap(QPixmap("./login/resource/images/background.jpg"))
        self.label.setScaledContents(True)
        self.horizontalLayout.addWidget(self.label)

        self.verticalLayout = QVBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        font = QFont()
        font.setFamily("楷体")
        font.setPointSize(18)

        self.label_2 = QLabel()
        self.label_2.setMaximumSize(QSize(16777215, 20))
        self.label_2.setFont(font)
        self.label_2.setText("教区名字")

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit_2 = LineEdit()
        self.lineEdit_2.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.lineEdit_2)

        self.label_3 = QLabel()
        self.label_3.setMaximumSize(QSize(16777215, 20))
        self.label_3.setFont(font)
        self.label_3.setText("建立日期")
        self.verticalLayout.addWidget(self.label_3)

        self.calendarPicker = CalendarPicker()
        self.calendarPicker.setMinimumSize(QSize(0, 40))
        # self.lineEdit_3.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.calendarPicker)

        self.label_5 = QLabel()
        self.label_5.setMaximumSize(QSize(16777215, 20))
        self.label_5.setFont(font)
        self.label_5.setText("当前主保")
        self.verticalLayout.addWidget(self.label_5)
        self.lineEdit_5 = LineEdit()
        self.verticalLayout.addWidget(self.lineEdit_5)
        # 设置当前日期
        self.calendarPicker.setDate(QDate(2024, 2, 26))

        self.label_4 = QLabel()
        self.label_4.setMaximumSize(QSize(16777215, 20))
        self.label_4.setFont(font)
        self.label_4.setText("地址")
        self.verticalLayout.addWidget(self.label_4)

        self.lineEdit_4 = LineEdit()
        self.lineEdit_4.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.lineEdit_4)


        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.BaseSchoolInterface_layout.addLayout(self.horizontalLayout)

    def get_InputSchoolDialoginfo(self):
        # 获取输入框中的数据并返回
        school_info = {
            'school_name': self.lineEdit_2.text(),
            'school_address': self.lineEdit_4.text(),
            'school_info': "self.textEdit.toPlainText()",
            'school_date': qdate_to_timestamp(self.calendarPicker.date),
            'school_pic_path': self.label.image_path
        }
        return school_info

    def set_school_info(self, school_info):
        # 设置学生信息
        self.lineEdit_2.setText(school_info['school_name'])
        self.lineEdit_4.setText(school_info['school_address'])
        qDate = timestamp_to_date(school_info["school_date"])
        # 设置文本框的文本为格式化后的日期时间
        self.calendarPicker.setDate(qDate)
        if school_info["school_pic_path"] is not None:
            if os.path.exists(school_info["school_pic_path"]):
                pixmap = QPixmap(school_info["school_pic_path"]).scaled(
                    self.label.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.label.setPixmap(pixmap)
