import enum
import time

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QHeaderView
from qfluentwidgets import MessageBoxBase, SubtitleLabel, InfoBar, PushButton

from BaseWidgets.BaseModule import BaseMainInterface, BaseMessageBoxWidget, BaseParishInterface
from DataBase.family_db import FamilyDB
from DataBase.parish_db import ParishDb
from DataBase.student_db import StudentDB
from Parishioner.family_interface import Family_MessageBox
from user.User_Interface import check_auth_permission
from utils.utils_tool import qdate_to_timestamp, timestamp_to_date


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class Parish_MessageBox(MessageBoxBase):

    def __init__(self, login_info, parent=None):
        super().__init__(parent)
        self.login_info = login_info
        self.family_info = None
        self.readOnly_flag = False
        self.set_reject_flag = False
        self.titleLabel = SubtitleLabel()
        self.Parishioner_Info_Edit_widgets = BaseParishInterface()
        self.Parishioner_Info_Edit_widgets.titleLabel.hide()
        self.Parishioner_Info_Edit_widgets.tailPic.hide()
        self.Parishioner_Info_Edit_widgets.button_1.hide()
        self.Parishioner_Info_Edit_widgets.button_2.hide()
        self.Parishioner_Info_Edit_widgets.mainPic.uploaded_image = True
        self.titleLabel.setText("堂区")
        self.widget.setMinimumWidth(600)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.Parishioner_Info_Edit_widgets)

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.Parishioner_Info_Edit_widgets.textEdit_1.text().strip():
            errors.append("请输入堂区名称")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.Parishioner_Info_Edit_widgets.textEdit_4.text().strip():
            errors.append("请输入地址")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.Parishioner_Info_Edit_widgets.textEdit_5.text().strip():
            errors.append("请输入本堂神父")  # 验证姓名是否填写，如果未填写，添加错误信息
        return errors  # 返回所有错误信息

    def validate(self):
        """ 重写验证表单数据的方法 """
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=1000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return False
        return True  # 返回验证结果，True 表示验证通过，False 表示验证失败


class Parish_Main_Interface(QWidget):
    def __init__(self, login_info, ObjectName):
        super().__init__()
        self.login_info = login_info
        # 创建主布局
        self.setObjectName(ObjectName)
        self.cur_parish_id = self.login_info['parish_id']
        self.cur_parish_info = None
        main_layout = QVBoxLayout(self)
        # self.setMinimumSize(500, 500)

        self.BaseMainInterface = BaseParishInterface()
        self.BaseMainInterface.titleLabel.setScaledContents(False)
        self.BaseMainInterface.textEdit_1.setReadOnly(True)
        self.BaseMainInterface.textEdit_2.setDisabled(True)
        self.BaseMainInterface.textEdit_3.setReadOnly(True)
        self.BaseMainInterface.textEdit_4.setReadOnly(True)
        self.BaseMainInterface.textEdit_5.setReadOnly(True)
        self.BaseMainInterface.textEdit_6.setReadOnly(True)
        # self.BaseMainInterface.titleLabel.setMinimumSize(100, 100)

        self.BaseMainInterface.label_2.setText("添加人员")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        pixmap = QPixmap("./resource/pic/main_head_1.png").scaled(
            self.BaseMainInterface.titleLabel.size() * 0.2,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.titleLabel.setPixmap(pixmap)

        pixmap = QPixmap("./resource/pic/main_tail.png").scaled(
            self.BaseMainInterface.tailPic.size()*0.28,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.tailPic.setPixmap(pixmap)
        self.Load_Parish()


    def resizeEvent(self, even):
        super().resizeEvent(even)
        pixmap = QPixmap("./resource/pic/main_head_1.png").scaled(
            self.BaseMainInterface.titleLabel.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.titleLabel.setPixmap(pixmap)

        pixmap = QPixmap("./resource/pic/main_tail.png").scaled(
            self.BaseMainInterface.tailPic.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.tailPic.setPixmap(pixmap)

    def Load_Parish(self):
        with ParishDb(self) as db:
            self.cur_parish_info = db.get_parish_info(self.cur_parish_id)

        print(self.cur_parish_info)
        if self.cur_parish_info is None:
            self.BaseMainInterface.mainPic.setText("先添加堂区信息")
        else:
            self.BaseMainInterface.setParishInfo(self.cur_parish_info)
            self.BaseMainInterface.button_2.clicked.connect(self.modify_parish)
        self.BaseMainInterface.button_2.setText("修改")
        self.BaseMainInterface.button_1.setText("添加")

        self.BaseMainInterface.button_1.clicked.connect(self.add_parish)


    @check_auth_permission(required_permission={"module_data": "parish", "permission_data": "add"})
    def add_parish(self):
        w = Parish_MessageBox(self.login_info, self)
        w.titleLabel.setText("添加堂区")
        if w.exec():
            with ParishDb(self) as db:
                get_InputParishMessageinfo = w.Parishioner_Info_Edit_widgets.getParishInfo()
                get_InputParishMessageinfo["operator"] = self.login_info["user_name"]
                get_InputParishMessageinfo["opera_time"] = int(time.time())
                if self.login_info["user_type"] != 0:
                    get_InputParishMessageinfo["opera_type"] = 0
                else:
                    get_InputParishMessageinfo["opera_type"] = 2
                db.add_parish(get_InputParishMessageinfo)
            return True
        return False

    @check_auth_permission(required_permission={"module_data": "parish", "permission_data": "modify"})
    def modify_parish(self):
        w = Parish_MessageBox(self.login_info, self)
        w.titleLabel.setText("修改堂区信息")
        w.Parishioner_Info_Edit_widgets.setParishInfo(self.cur_parish_info)
        if w.exec():
            with ParishDb(self) as db:
                get_InputParishMessageinfo = w.Parishioner_Info_Edit_widgets.getParishInfo()
                get_InputParishMessageinfo["operator"] = self.login_info["user_name"]
                get_InputParishMessageinfo["opera_time"] = int(time.time())
                if self.login_info["user_type"] != 0:
                    get_InputParishMessageinfo["opera_type"] = 0
                else:
                    get_InputParishMessageinfo["opera_type"] = 2
                db.modify_parish(get_InputParishMessageinfo)
            return True
        return False

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login_info_1 = {
        "parish_id": 1,
        "parish_name": "崇义堂区",
        "user_id": 1,
        "user_name": "admin",
        "user_type": 1,
        "user_authnum": 32767
    }
    main_window = Parish_Main_Interface(login_info_1, 'testParishioner_Main_Interface')
    main_window.resize(1000, 800)
    main_window.show()


    sys.exit(app.exec())
