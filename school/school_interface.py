import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLabel, QSizePolicy, QLineEdit, \
    QTextBrowser
from qfluentwidgets import PushButton, setCustomStyleSheet, MessageBoxBase

from utils.custom_style import ADD_BUTTON_STYLE, DELETE_BUTTON_STYLE


class BaseSchoolInterface_Temp():
    def __init__(self):
        self.BaseSchoolInterface_layout = QVBoxLayout()

        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel()
        self.label_title = QLabel()

        self.verticalLayout = QVBoxLayout()
        self.label_2 = QLabel()
        self.lineEdit_2 = QLineEdit()
        self.label_3 = QLabel()
        self.lineEdit_3 = QLineEdit()
        self.label_4 = QLabel()
        self.lineEdit_4 = QLineEdit()
        self.textBrowser = QTextBrowser()

        self.setup_ui()

    def setup_ui(self):
        self.label.setMinimumSize(QSize(400, 400))
        self.label.setMaximumSize(QSize(500, 500))
        self.label.setText("")
        self.label.setPixmap(QPixmap("./login/resource/images/background.jpg"))
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

        self.lineEdit_3.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.lineEdit_3)

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
        self.BaseSchoolInterface_layout.addWidget(self.textBrowser)


class AddSchoolInterface(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.viewLayout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.schoolInterface_temp.label_title.setText("添加学校")
        self.setObjectName("AddSchoolInterface")
        self.school_id = None  # 初始化学生 ID 属性，默认为 None，表示新建学生时不需要指定 ID
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能


class ModifySchoolInterface(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.viewLayout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.schoolInterface_temp.label_title.setText("修改学校")
        self.setObjectName("ModifySchoolInterface")
        self.school_id = None  # 初始化学生 ID 属性，默认为 None，表示新建学生时不需要指定 ID
        self.yesButton.setText('修改')  # 设置确认按钮的文本为“添加”，以明确功能


# 该布局为主界面显示布局，无法继承message类，所有与弹出后修改或添加布局分开，布局内容基本一致，该布局从UI文件加载
class ShowSchoolInterface(QWidget):
    def __init__(self, curSchool):
        super().__init__()
        self.setObjectName("ShowSchoolInterface")
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.setupUi()
        self.disable_widgets()

        if curSchool is None:
            self.schoolInterface_temp.label.setText("请先选择或建立学校")
        else:
            self.schoolInterface_temp.lineEdit_3.setText(str(curSchool["school_date"]))
            self.schoolInterface_temp.lineEdit_2.setText(curSchool["school_name"])
            self.schoolInterface_temp.lineEdit_4.setText(curSchool["school_address"])
            self.schoolInterface_temp.textBrowser.setText(curSchool["school_info"])
            pixmap = QPixmap("./login/resource/images/background.jpg").scaled(
                self.schoolInterface_temp.label.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.schoolInterface_temp.label.setPixmap(pixmap)

    def setupUi(self):
        self.addButton = PushButton('Add', self)
        setCustomStyleSheet(self.addButton, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)
        self.addButton.clicked.connect(self.addSchoolInfo)

        self.modifyButton = PushButton('Modify', self)
        setCustomStyleSheet(self.modifyButton, DELETE_BUTTON_STYLE, DELETE_BUTTON_STYLE)
        self.modifyButton.clicked.connect(self.modifySchoolInfo)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.addButton)
        self.horizontalLayout.addWidget(self.modifyButton)
        self.main_layout.addLayout(self.horizontalLayout)

    def disable_widgets(self):
        self.schoolInterface_temp.lineEdit_4.setReadOnly(True)
        self.schoolInterface_temp.lineEdit_2.setReadOnly(True)
        self.schoolInterface_temp.lineEdit_3.setReadOnly(True)
        self.schoolInterface_temp.textBrowser.setReadOnly(True)

    def addSchoolInfo(self):
        w = AddSchoolInterface(self)
        if w.exec():
            pass

    def modifySchoolInfo(self):
        w = ModifySchoolInterface(self)
        if w.exec():
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShowSchoolInterface(None)
    window.show()
    sys.exit(app.exec())
