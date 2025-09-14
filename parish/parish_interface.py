import sys

from PyQt6 import QtGui, QtCore
from PyQt6.QtCharts import QPieSeries, QChartView, QChart, QLineSeries, QValueAxis
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QLabel
from qfluentwidgets import PushButton, setCustomStyleSheet, MessageBoxBase, InfoBar, CardWidget

from DataBase.family_db import FamilyDB
from DataBase.parish_db import ParishDb
from parish.parish_dialog import BaseSchoolInterface_Temp
from utils.custom_style import ADD_BUTTON_STYLE, DELETE_BUTTON_STYLE, UPDATE_BUTTON_STYLE


class AddSchoolInterface(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.schoolInterface_temp.label.uploaded_image = True
        self.viewLayout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.setObjectName("AddSchoolInterface")
        self.school_id = None
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能

    def _validateInput(self):
        errors = []  # 初始化错误信息列表
        # 验证学校名称
        parish_name = self.schoolInterface_temp.lineEdit_2.text()
        if not parish_name:
            errors.append("教区名称不能为空")
        elif len(parish_name) > 20:
            errors.append("教区名称不能超过20个字符")
        else:
            with ParishDb(self) as db:
                if db.check_parish_name(parish_name):
                    errors.append("教区名称已存在")

        parish_address = self.schoolInterface_temp.lineEdit_4.text()
        if not parish_address:
            errors.append("教区地址不能为空")

        parish_info = self.schoolInterface_temp.lineEdit_5.text()
        if not parish_info:
            errors.append("当前主保不能为空")

        parish_info = self.schoolInterface_temp.lineEdit_6.text()
        if not parish_info:
            errors.append("本堂神父不能为空")
        parish_info = self.schoolInterface_temp.lineEdit_7.text()
        if not parish_info:
            errors.append("联系电话不能为空")
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


class ModifyParishInterface(MessageBoxBase):
    def __init__(self, parish_info, parent=None):
        super().__init__(parent)
        self.schoolInterface_temp = BaseSchoolInterface_Temp()
        self.viewLayout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.schoolInterface_temp.label.uploaded_image = True
        self.setObjectName("ModifyParishInterface")
        self.parish_id = None  #
        self.yesButton.setText('修改')  # 设置确认按钮的文本为“添加”，以明确功能

        self.schoolInterface_temp.set_parish_info(parish_info)
        #self.schoolInterface_temp.lineEdit_2.setReadOnly(True)

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        parish_address = self.schoolInterface_temp.lineEdit_4.text()
        if not parish_address:
            errors.append("教区地址不能为空")

        parish_info = self.schoolInterface_temp.lineEdit_5.text()
        if not parish_info:
            errors.append("当前主保不能为空")

        parish_info = self.schoolInterface_temp.lineEdit_6.text()
        if not parish_info:
            errors.append("本堂神父不能为空")
        parish_info = self.schoolInterface_temp.lineEdit_7.text()
        if not parish_info:
            errors.append("联系电话不能为空")
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
    def __init__(self, login_info, object_name):
        super().__init__()
        self.login_info = login_info

        self.setObjectName(object_name)
        self.schoolInterface_temp = BaseSchoolInterface_Temp()

        self.main_layout = QVBoxLayout(self)
        self.title_pic = QLabel(self)
        pixmap = QPixmap("./resource/pic/main_head_1.png").scaled(
            self.title_pic.size()*5,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.title_pic.setPixmap(pixmap)
        self.main_layout.addWidget(self.title_pic)
        self.main_layout.addLayout(self.schoolInterface_temp.BaseSchoolInterface_layout)
        self.tail_pic = QLabel(self)
        pixmap = QPixmap("./resource/pic/main_tail.png").scaled(
            self.tail_pic.size()*5,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.tail_pic.setPixmap(pixmap)
        self.main_layout.addWidget(self.tail_pic)

        self.setupUi()
        self.disable_widgets()

        if self.login_info["parish_id"] is None:
            self.schoolInterface_temp.label.setText("请先选择或建立教区")
            self.schoolInterface_temp.label.uploaded_image = False
            self.modifyButton.setDisabled(True)
        else:
            # 将时间戳转换为日期时间格式
            from DataBase.parish_db import ParishDb
            with ParishDb(self) as db:
                parish_info = db.get_parish_info(self.login_info["parish_id"])
                self.schoolInterface_temp.set_parish_info(parish_info)

    def setupUi(self):
        self.addButton = PushButton('添加', self)
        setCustomStyleSheet(self.addButton, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)
        # noinspection PyUnresolvedReferences
        self.addButton.clicked.connect(self.addSchoolInfo)

        self.modifyButton = PushButton('修改', self)
        setCustomStyleSheet(self.modifyButton, DELETE_BUTTON_STYLE, DELETE_BUTTON_STYLE)
        # noinspection PyUnresolvedReferences
        self.modifyButton.clicked.connect(self.modifySchoolInfo)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.addWidget(self.addButton)
        self.horizontalLayout.addWidget(self.modifyButton)
        # self.horizontalLayout.addWidget(self.setButton)
        self.schoolInterface_temp.BaseSchoolInterface_layout.addLayout(self.horizontalLayout)
    def disable_widgets(self):
        self.schoolInterface_temp.lineEdit_4.setReadOnly(True)
        self.schoolInterface_temp.lineEdit_2.setReadOnly(True)
        self.schoolInterface_temp.calendarPicker.setDisabled(True)

    def addSchoolInfo(self):
        w = AddSchoolInterface(self)
        if w.exec():
            with ParishDb(self) as db:
                db.add_parish(w.schoolInterface_temp.get_InputParishDialoginfo())
                self.restartButton = PushButton('重启以重新选择教区', self)
                setCustomStyleSheet(self.restartButton, UPDATE_BUTTON_STYLE, UPDATE_BUTTON_STYLE)
                self.horizontalLayout.addWidget(self.restartButton)
                # self.restartButton.clicked.connect(self.parent.on_back_to_login)

    def modifySchoolInfo(self):
        w = ModifyParishInterface(self.schoolInterface_temp.get_InputParishDialoginfo(), self)
        if w.exec():
            with ParishDb(self) as db:
                db.modify_parish(w.schoolInterface_temp.get_InputParishDialoginfo())
                self.schoolInterface_temp.set_parish_info(w.schoolInterface_temp.get_InputParishDialoginfo())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ParishInfoShowInfo()
    window.show()
    sys.exit(app.exec())
