from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QHeaderView, QCheckBox, QTableWidgetItem, \
    QLabel, QSizePolicy, QLineEdit, QTextBrowser
from qfluentwidgets import CardWidget, PushButton, SearchLineEdit, TableWidget, setCustomStyleSheet, MessageBoxBase, \
    SubtitleLabel, LineEdit

from student.student_dialog import AddStudentDialog
from utils.custom_style import ADD_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE, DELETE_BUTTON_STYLE
from school.school_from_base import Ui_Form
from DataBase.school_db import SchoolDb
import sys


class UI_SchoolInterface(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class BaseSchoolInterface(MessageBoxBase):
    def __init__(self, title, parent=None):
        super().__init__(parent)  # 调用父类的初始化方法，设置父窗口
        self.title = title  # 保存弹窗标题，用于区分弹窗用途（如添加或修改学生信息）
        self.setObjectName("BaseSchoolInterface")
        self.setupUi()

    def setupUi(self):
        self.titleLabel = SubtitleLabel(self.title, self)  # 创建一个 SubtitleLabel 实例，传入标题文本和父窗口
        self.viewLayout.addWidget(self.titleLabel)  # 将标题控件添加到布局中
        self.viewLayout.setAlignment(self.titleLabel, Qt.AlignmentFlag.AlignCenter)  # 设置标题控件在布局中的对齐方式为居中

        self.horizontalLayout = QHBoxLayout()

        self.label = QLabel()
        self.label.setMinimumSize(QSize(400, 400))
        self.label.setMaximumSize(QSize(500, 500))
        self.label.setText("")
        self.label.setPixmap(QPixmap("./login/resource/images/background.jpg"))
        self.label.setScaledContents(True)
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout = QVBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QLabel()
        self.label_2.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setText("教区名字")
        self.verticalLayout.addWidget(self.label_2)


        self.lineEdit_2 = QLineEdit()
        self.lineEdit_2.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.lineEdit_2)

        self.label_3 = QLabel()
        self.label_3.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setText("建立日期")
        self.verticalLayout.addWidget(self.label_3)

        self.lineEdit = QLineEdit()
        self.lineEdit.setMinimumSize(QSize(0, 40))
        self.verticalLayout.addWidget(self.lineEdit)

        self.label_4 = QLabel()
        self.label_4.setMaximumSize(QSize(16777215, 20))
        font = QFont()
        font.setFamily("楷体")
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setText("地址")
        self.verticalLayout.addWidget(self.label_4)

        self.lineEdit_3 = QLineEdit()
        self.lineEdit_3.setMinimumSize(QSize(0, 40))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout.addWidget(self.lineEdit_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.viewLayout.addLayout(self.horizontalLayout)

        self.textBrowser = QTextBrowser()
        self.viewLayout.addWidget(self.textBrowser)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.viewLayout.addLayout(self.horizontalLayout_3)


class AddStudentInterface(BaseSchoolInterface):
    def __init__(self, parent=None):
        super().__init__('添加学生', parent)
        self.setObjectName("AddSchoolInterface")
        self.school_id = None  # 初始化学生 ID 属性，默认为 None，表示新建学生时不需要指定 ID
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能


class ModifyStudentInterface(BaseSchoolInterface):
    def __init__(self):
        super().__init__('修改学校')
        self.setObjectName("ModifySchoolInterface")
        self.school_id = None  # 初始化学生 ID 属性，默认为 None，表示新建学生时不需要指定 ID
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能


class ShowSchoolInterface(UI_SchoolInterface):
    def __init__(self, curSchool, parent=None):
        super().__init__()
        self.curSchool = curSchool
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.textBrowser.setReadOnly(True)
        self.setup_ui()

        if curSchool is None:
            self.label.setText("请先选择或建立学校")
        else:
            self.lineEdit.setText(str(curSchool["school_date"]))
            self.lineEdit_2.setText(curSchool["school_name"])
            self.lineEdit_3.setText(curSchool["school_address"])
            self.textBrowser.setText(curSchool["school_info"])
            pixmap = QPixmap("./login/resource/images/background.jpg").scaled(
                self.label.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(pixmap)

    def setup_ui(self):
        self.addButton = PushButton('Add', self)
        setCustomStyleSheet(self.addButton, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)
        self.addButton.clicked.connect(self.addSchoolInfo)

        self.modifyButton = PushButton('Modify', self)
        setCustomStyleSheet(self.modifyButton, DELETE_BUTTON_STYLE, DELETE_BUTTON_STYLE)
        self.modifyButton.clicked.connect(self.modifySchoolInfo)

        self.horizontalLayout_3.addWidget(self.addButton)
        self.horizontalLayout_3.addWidget(self.modifyButton)

    def addSchoolInfo(self):
        w = AddStudentInterface(self)
        if w.exec():
            pass

    def modifySchoolInfo(self):
        w = ModifyStudentInterface()
        if w.exec():
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShowSchoolInterface(None)
    window.show()
    sys.exit(app.exec())
