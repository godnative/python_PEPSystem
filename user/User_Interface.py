import enum
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import MessageBoxBase, SubtitleLabel, InfoBar

from BaseWidgets.BaseModule import BaseMainInterface, BaseUserInterface
from DataBase.user_db import UserDB
from utils.msyscfg import CUR_SYS_TYPE

check_module_data = {
    "parishioner": 0,
    "family": 1,
    "event": 2,
    "parish": 3,
    "user": 4
}

check_permission_data = {
    "add": 0,
    "delete": 1,
    "modify": 2
}


def check_bit_at_position(num, position):
    """
    判断一个数的指定二进制位是否为 1
    :param num: 输入的整数
    :param position: 要检查的二进制位的位置，从 0 开始计数
    :return: 如果指定位置的二进制位为 1，返回 True；否则返回 False
    """
    if type(position) is not int:
        return False
    return (num & (1 << position)) != 0


# 定义一个装饰器函数
def check_auth_permission(required_permission):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 检查用户是否有操作权限
            self = args[0]
            authnum = self.login_info["user_authnum"]
            check_pos = (check_module_data[required_permission["module_data"]] * 3 +
                         check_permission_data[required_permission["permission_data"]])
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            if check_bit_at_position(authnum, check_pos):
                # 如果有操作权限，执行原函数
                ret = func(self)
                if CUR_SYS_TYPE == 0 and ret:
                    with UserDB(self) as db:
                        exec_log = "[%s] 执行 %s %s 操作 成功" % (
                            formatted_time,
                            required_permission["module_data"],
                            required_permission["permission_data"])
                        db.add_user_log({"user_id": self.login_info["user_id"], "user_log_info": exec_log})
                        InfoBar.success(title="操作成功", content=exec_log, parent=self,
                                        duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
                return
            else:
                # 如果没有操作权限，打印失败消息并退出
                exec_log = "[%s] 用户：%s 执行 %s %s 操作 失败[权限不足]" % (
                    self.login_info["user_name"],
                    formatted_time,
                    required_permission["module_data"],
                    required_permission["permission_data"])
                InfoBar.error(title="权限错误", content=exec_log, parent=self,
                              duration=1000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
                exec_log = "[%s] 执行 %s 操作 失败[权限不足]" % (formatted_time, required_permission)
                print(exec_log)
                if CUR_SYS_TYPE == 0:
                    with UserDB(self) as db:
                        db.add_user_log({"user_id": self.login_info["user_id"], "user_log_info": exec_log})
            return None

        return wrapper

    return decorator


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class User_MessageBox(MessageBoxBase):

    def __init__(self, massage_type, parent=None):
        super().__init__(parent)
        self.family_info = None
        self.massage_type = massage_type
        self.titleLabel = SubtitleLabel('人员', self)
        self.User_info_edit_widgets = BaseUserInterface(self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.User_info_edit_widgets)

        self.User_info_edit_widgets.BaseQuery.tableWidget.hide()
        if massage_type == 1:
            self.User_info_edit_widgets.line_name.setReadOnly(True)
            self.User_info_edit_widgets.line_type.setDisabled(True)
            self.User_info_edit_widgets.line_password.setReadOnly(True)
            self.User_info_edit_widgets.line_note.setReadOnly(True)
            self.User_info_edit_widgets.set_all_checkbox_state(False)

        self.User_info_edit_widgets.label.setMaximumSize(100, 100)
        pixmap = QPixmap("./resource/pic/2.png").scaled(
            self.User_info_edit_widgets.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.User_info_edit_widgets.label.setPixmap(pixmap)

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.User_info_edit_widgets.line_name.text().strip():
            errors.append("请输入用户名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if self.massage_type == 0:
            with UserDB(self) as db:
                if db.check_user_name_exists(self.User_info_edit_widgets.line_name.text().strip()):
                    errors.append("用户名已存在")  # 验证学号是否填写，如果未填写，添加错误信息

        if not self.User_info_edit_widgets.label_password.text().strip():
            errors.append("请输入密码")  # 验证学号是否填写，如果未填写，添加错误信息

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

    def get_InputUserMessageinfo(self):
        user_messageinfo = {
            "user_name": self.User_info_edit_widgets.line_name.text(),
            "user_type": self.User_info_edit_widgets.line_type.currentIndex(),
            "user_password": self.User_info_edit_widgets.line_password.text(),  # 性别字段与对应的下拉框
            "user_note": self.User_info_edit_widgets.line_note.text(),  # 班级字段与对应的下拉框
            "user_authnum": self.User_info_edit_widgets.get_bitmap_from_checkbox_state()
        }
        return user_messageinfo

    def set_InputUserMessageinfo(self, user_messageinfo):
        """
        将传入的用户信息字典中的参数加载到 self.User_info_edit_widgets 中
        :param user_messageinfo: 包含用户信息的字典，键为字段名，值为对应的值
        """
        self.User_info_edit_widgets.line_name.setText(user_messageinfo["user_name"])
        self.User_info_edit_widgets.line_type.setCurrentIndex(user_messageinfo["user_type"])
        self.User_info_edit_widgets.line_password.setText(user_messageinfo["user_password"])
        self.User_info_edit_widgets.line_note.setText(user_messageinfo["user_note"])
        self.User_info_edit_widgets.set_checkbox_state_from_bitmap(user_messageinfo["user_authnum"])


class User_Show_Interface(QWidget):
    def __init__(self, login_info, ObjectName):
        super().__init__()
        self.login_info = login_info
        # 创建主布局
        self.user_log_all = None
        self.setObjectName(ObjectName)
        self.parishioner_info_all = None
        self.cur_parish_id = self.login_info['parish_id']
        main_layout = QVBoxLayout(self)
        self.setMinimumSize(500, 500)

        self.BaseUserInterface = BaseUserInterface(self)
        self.BaseUserInterface.label.setMinimumSize(100, 100)

        pixmap = QPixmap("./resource/pic/1.png").scaled(
            self.BaseUserInterface.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseUserInterface.label.setPixmap(pixmap)

        main_layout.addWidget(self.BaseUserInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        self.BaseUserInterface.set_all_checkbox_state(False)
        self.BaseUserInterface.line_password.hide()
        self.BaseUserInterface.label_password.hide()
        self.BaseUserInterface.line_name.setReadOnly(True)
        self.BaseUserInterface.line_type.setDisabled(True)
        self.BaseUserInterface.line_note.setReadOnly(True)

        self.user_log_tableView_header = [
            "用户名称", "用户类型", "用户操作", ""
        ]
        self.BaseUserInterface.BaseQuery.tableWidget.setColumnCount(len(self.user_log_tableView_header))
        self.BaseUserInterface.BaseQuery.tableWidget.setHorizontalHeaderLabels(self.user_log_tableView_header)
        self.Load_User_Log(self.login_info["user_id"])
        with UserDB(self) as db:
            user_info = db.fetch_users_from_id(self.login_info["user_id"])
        self.BaseUserInterface.set_user_info(user_info)

    def Load_User_Log(self, user_id):
        with UserDB(self) as db:
            self.user_log_all = db.fetch_user_log(user_id, 10)
            print(self.user_log_all)

        if self.user_log_all is None:
            return

        header_info = [
            'user_name', 'user_type', 'user_log_info'
        ]
        self.BaseUserInterface.BaseQuery.set_viewWidget_data(header_info, self.user_log_all)

    def add_parishioner(self):
        print(self.BaseUserInterface.get_bitmap_from_checkbox_state())

    def set_parishioner(self):
        self.BaseUserInterface.set_checkbox_state_from_bitmap(8063)


class User_Modify_Interface(QWidget):
    def __init__(self, ObjectName):
        super().__init__()

        # 创建主布局
        self.setObjectName(ObjectName)
        self.user_info_all = None
        main_layout = QVBoxLayout(self)
        self.setMinimumSize(500, 500)

        self.BaseMainInterface = BaseMainInterface(self)
        self.BaseMainInterface.label.setMinimumSize(100, 100)

        pixmap = QPixmap("./resource/pic/8.png").scaled(
            self.BaseMainInterface.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.label.setPixmap(pixmap)
        self.BaseMainInterface.label_2.setText("修改用户信息")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        self.BaseMainInterface.BaseQuery.addButton.clicked.connect(self.add_user)
        self.BaseMainInterface.BaseQuery.delButton.clicked.connect(self.delete_user)
        self.BaseMainInterface.BaseQuery.ModButton.clicked.connect(self.modify_user)
        self.BaseMainInterface.BaseQuery.searchInput.searchSignal.connect(self.query_user_info_with_like)
        self.BaseMainInterface.BaseQuery.searchInput.returnPressed.connect(self.query_user_info_with_like)

        self.user_tableView_header = [
            "用户名称", "用户类型", "简介"," "
        ]
        self.BaseMainInterface.BaseQuery.tableWidget.setColumnCount(len(self.user_tableView_header))
        self.BaseMainInterface.BaseQuery.tableWidget.setHorizontalHeaderLabels(self.user_tableView_header)
        self.Load_User(QUERY_TYPE.QUERY_ALL)

    def query_user_info_with_like(self):
        if self.BaseMainInterface.BaseQuery.searchInput.text() == "":
            self.Load_User(QUERY_TYPE.QUERY_ALL)
        else:
            self.Load_User(QUERY_TYPE.QUERY_LIKE, self.BaseMainInterface.BaseQuery.searchInput.text())

    def Load_User(self, query_type, query_param=None):
        with UserDB(self) as db:
            if query_type == QUERY_TYPE.QUERY_ALL:
                self.user_info_all = db.fetch_all_users()
            elif query_type == QUERY_TYPE.QUERY_LIKE:
                self.user_info_all = db.fetch_user_with_likestr(query_param)
            else:
                return

        if self.user_info_all is None:
            return

        header_info = [
            'user_name', 'user_type', 'user_note'
        ]
        self.BaseMainInterface.BaseQuery.set_viewWidget_data(header_info, self.user_info_all)

    def add_user(self):
        w = User_MessageBox(0, self)
        w.User_info_edit_widgets.set_checkbox_state_from_bitmap(32767)
        w.titleLabel.setText("添加用户")
        if w.exec():
            with UserDB(self) as db:
                get_InputUserMessageinfo = w.get_InputUserMessageinfo()
                print("get data")
                db.add_user(get_InputUserMessageinfo)
                print(get_InputUserMessageinfo)
            self.Load_User(QUERY_TYPE.QUERY_ALL)

    def delete_user(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = User_MessageBox(1, self)
            w.titleLabel.setText("添加用户")
            w.set_InputUserMessageinfo(self.user_info_all[idx])
            if w.exec():
                with UserDB(self) as db:
                    db.delete_user(self.user_info_all[idx]["user_id"])
                self.Load_User(QUERY_TYPE.QUERY_ALL)

    def modify_user(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = User_MessageBox(2, self)
            w.titleLabel.setText("修改用户信息")
            w.set_InputUserMessageinfo(self.user_info_all[idx])
            if w.exec():
                with UserDB(self) as db:
                    parishioner_info = w.get_InputUserMessageinfo()
                    parishioner_info["user_id"] = self.user_info_all[idx]["user_id"]
                    db.update_user(parishioner_info)
                self.Load_User(QUERY_TYPE.QUERY_ALL)
