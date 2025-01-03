import pickle
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication
from qfluentwidgets import PushButton, setCustomStyleSheet, MessageBoxBase, InfoBar, Flyout, InfoBarIcon

from DataBase.school_db import SchoolDb
from school.school_dialog import BaseSchoolInterface_Temp
from utils.custom_style import ADD_BUTTON_STYLE, DELETE_BUTTON_STYLE, UPDATE_BUTTON_STYLE, IMPORT_BUTTON_STYLE
from utils.utils_tool import timestamp_to_date


class AddSchoolInterface(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.schoolInterface_temp.label.uploaded_image = True
        self.viewLayout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.schoolInterface_temp.label_title.setText("添加学校")
        self.setObjectName("AddSchoolInterface")
        self.school_id = None
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能

    def _validateInput(self):
        errors = []  # 初始化错误信息列表
        # 验证学校名称
        school_name = self.schoolInterface_temp.lineEdit_2.text()
        if not school_name:
            errors.append("学校名称不能为空")
        elif len(school_name) > 20:
            errors.append("学校名称不能超过20个字符")
        else:
            with SchoolDb() as db:
                if db.check_school_name(school_name):
                    errors.append("学校名称已存在")
        # 验证学校地址
        school_address = self.schoolInterface_temp.lineEdit_4.text()
        if not school_address:
            errors.append("学校地址不能为空")

        # 验证学校简介
        school_info = self.schoolInterface_temp.textEdit.toPlainText()
        if not school_info:
            errors.append("学校简介不能为空")
        # 返回错误信息列表，如果为空则表示验证通过
        return errors

    def accept(self):
        # 对数据进行验证
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        # 如果验证通过，调用父类的 accept 方法，接收数据并关闭对话框
        super().accept()


class ModifySchoolInterface(MessageBoxBase):
    def __init__(self, school_info, parent=None):
        super().__init__(parent)
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.viewLayout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.schoolInterface_temp.label_title.setText("修改学校")
        self.setObjectName("ModifySchoolInterface")
        self.school_id = None  # 初始化学生 ID 属性，默认为 None，表示新建学生时不需要指定 ID
        self.yesButton.setText('修改')  # 设置确认按钮的文本为“添加”，以明确功能

        self.schoolInterface_temp.set_school_info(school_info)
        self.schoolInterface_temp.lineEdit_2.setReadOnly(True)

    def _validateInput(self):
        errors = []  # 初始化错误信息列表
        # 验证学校地址
        school_address = self.schoolInterface_temp.lineEdit_4.text()
        if not school_address:
            errors.append("学校地址不能为空")

        # 验证学校简介
        school_info = self.schoolInterface_temp.textEdit.toPlainText()
        if not school_info:
            errors.append("学校简介不能为空")
        # 返回错误信息列表，如果为空则表示验证通过
        return errors

    def accept(self):
        # 对数据进行验证
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        # 如果验证通过，调用父类的 accept 方法，接收数据并关闭对话框
        super().accept()


# 该布局为主界面显示布局，无法继承message类，所有与弹出后修改或添加布局分开，布局内容基本一致，该布局从UI文件加载
class ShowSchoolInterface(QWidget):
    def __init__(self, curSchool, parent=None):
        super().__init__()
        self.parent = parent
        self.curSchool = curSchool
        self.setObjectName("ShowSchoolInterface")
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.setupUi()
        self.disable_widgets()

        if curSchool is None:
            self.schoolInterface_temp.label.setText("请先选择或建立学校")
        else:
            # 将时间戳转换为日期时间格式

            qDate = timestamp_to_date(curSchool["school_date"])
            # 设置文本框的文本为格式化后的日期时间
            self.schoolInterface_temp.calendarPicker.setDate(qDate)

            self.schoolInterface_temp.lineEdit_2.setText(curSchool["school_name"])
            self.schoolInterface_temp.lineEdit_4.setText(curSchool["school_address"])
            self.schoolInterface_temp.textEdit.setText(curSchool["school_info"])
            pixmap = QPixmap("./login/resource/images/background.jpg").scaled(
                self.schoolInterface_temp.label.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.schoolInterface_temp.label.setPixmap(pixmap)

    def setupUi(self):
        self.addButton = PushButton('添加', self)
        setCustomStyleSheet(self.addButton, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)
        self.addButton.clicked.connect(self.addSchoolInfo)

        self.modifyButton = PushButton('修改', self)
        setCustomStyleSheet(self.modifyButton, DELETE_BUTTON_STYLE, DELETE_BUTTON_STYLE)
        self.modifyButton.clicked.connect(self.modifySchoolInfo)

        self.setButton = PushButton('设置默认教堂', self)
        setCustomStyleSheet(self.modifyButton, IMPORT_BUTTON_STYLE, IMPORT_BUTTON_STYLE)
        self.setButton.clicked.connect(self.show_setschool_Flyout1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.addButton)
        self.horizontalLayout.addWidget(self.modifyButton)
        self.horizontalLayout.addWidget(self.setButton)
        self.main_layout.addLayout(self.horizontalLayout)

    def show_setschool_Flyout1(self):
        print(self.curSchool)
        if self.curSchool is not None:
            content = "成功设置：%s 为默认教堂" % self.curSchool["school_name"]
            icon = InfoBarIcon.SUCCESS
            with open("./schoolsetting.pkl", 'wb') as f:
                pickle.dump(self.curSchool, f)
        else:
            content = "设置失败"
            icon = InfoBarIcon.ERROR

        Flyout.create(
            icon=icon,
            title='设置默认教堂',
            content=content,
            target=self.setButton,
            parent=self,
            isClosable=True
        )
    def disable_widgets(self):
        self.schoolInterface_temp.lineEdit_4.setReadOnly(True)
        self.schoolInterface_temp.lineEdit_2.setReadOnly(True)
        self.schoolInterface_temp.calendarPicker.setDisabled(True)
        self.schoolInterface_temp.textEdit.setReadOnly(True)

    def addSchoolInfo(self):
        w = AddSchoolInterface(self)
        if w.exec():
            with SchoolDb() as db:
                db.add_school(w.schoolInterface_temp.get_InputSchoolDialoginfo())
                self.restartButton = PushButton('重启以重新选择学校', self)
                setCustomStyleSheet(self.restartButton, UPDATE_BUTTON_STYLE, UPDATE_BUTTON_STYLE)
                self.horizontalLayout.addWidget(self.restartButton)
                self.restartButton.clicked.connect(self.parent.on_back_to_login)

    def modifySchoolInfo(self):
        w = ModifySchoolInterface(self.schoolInterface_temp.get_InputSchoolDialoginfo(), self)
        if w.exec():
            with SchoolDb() as db:
                db.modify_school(w.schoolInterface_temp.get_InputSchoolDialoginfo())
                self.schoolInterface_temp.set_school_info(w.schoolInterface_temp.get_InputSchoolDialoginfo())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShowSchoolInterface(None)
    window.show()
    sys.exit(app.exec())
