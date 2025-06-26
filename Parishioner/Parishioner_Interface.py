import enum
import time

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QHeaderView
from qfluentwidgets import MessageBoxBase, SubtitleLabel, InfoBar

from BaseWidgets.BaseModule import BaseMainInterface, BaseMessageBoxWidget
from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from Parishioner.family_interface import Family_MessageBox
from user.User_Interface import check_auth_permission
from utils.utils_tool import qdate_to_timestamp, timestamp_to_date


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class Parishioner_MessageBox(MessageBoxBase):

    def __init__(self, login_info, parent=None):
        super().__init__(parent)
        self.login_info = login_info
        self.family_info = None
        self.readOnly_flag = False
        self.set_reject_flag = False
        self.titleLabel = SubtitleLabel('人员', self)
        self.Parishioner_Info_Edit_widgets = BaseMessageBoxWidget(self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.Parishioner_Info_Edit_widgets)

        # 设置UI
        self.Parishioner_Info_Edit_widgets.label_1.setText("姓名")
        self.Parishioner_Info_Edit_widgets.label_2.setText("圣名")
        self.Parishioner_Info_Edit_widgets.label_3.setText("手机")
        # self.Parishioner_Info_Edit_widgets.label_4.setText("身份证")
        self.Parishioner_Info_Edit_widgets.label_9.setText("性别")
        self.Parishioner_Info_Edit_widgets.label_10.setText("出生日期")
        self.Parishioner_Info_Edit_widgets.inputLine_10.setDate(QDate(2025, 1, 1))
        self.Parishioner_Info_Edit_widgets.label_11.setText("家庭")
        self.Parishioner_Info_Edit_widgets.inputLine_12.setText("添加家庭")
        self.Parishioner_Info_Edit_widgets.label_13.setText("备注")

        self.Parishioner_Info_Edit_widgets.label_4.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_4.hide()
        self.Parishioner_Info_Edit_widgets.label_5.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_5.hide()
        self.Parishioner_Info_Edit_widgets.label_6.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_6.hide()
        self.Parishioner_Info_Edit_widgets.label_7.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_7.hide()
        self.Parishioner_Info_Edit_widgets.label_8.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_8.hide()
        # self.Parishioner_Info_Edit_widgets.label_12.hide()
        self.Parishioner_Info_Edit_widgets.label_12.setText("     ")

        self.Parishioner_Info_Edit_widgets.inputLine_9.addItem("男", userData=0)
        self.Parishioner_Info_Edit_widgets.inputLine_9.addItem("女", userData=1)

        self.Parishioner_Info_Edit_widgets.pic.setMaximumSize(100, 100)
        pixmap = QPixmap("./resource/pic/2.png").scaled(
            self.Parishioner_Info_Edit_widgets.pic.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        if self.login_info["user_type"] == 0:
            from qfluentwidgets import PushButton
            self.rejectButton = PushButton("重新录入")
            self.buttonLayout.addWidget(self.rejectButton, 1)
            self.rejectButton.clicked.connect(self.setRejected)

        self.Parishioner_Info_Edit_widgets.pic.setPixmap(pixmap)

        self.widget.setMinimumWidth(350)
        self.Parishioner_Info_Edit_widgets.inputLine_12.clicked.connect(self.add_family)
        self.load_family()

    def setRejected(self):
        self.set_reject_flag = True
        self.accept()
    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.Parishioner_Info_Edit_widgets.inputLine_1.text().strip():
            errors.append("请输入姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if self.Parishioner_Info_Edit_widgets.inputLine_11.currentData() is None:
            errors.append("请选择家庭")  # 验证学号是否填写，如果未填写，添加错误信息

        if self.Parishioner_Info_Edit_widgets.inputLine_9.currentData() is None:
            errors.append("请选择性别")  # 验证班级是否选择，如果未选择班级，添加错误信息

        return errors  # 返回所有错误信息

    def add_family(self):
        w = Family_MessageBox(self.login_info, 0, self)
        w.titleLabel.setText("添加家庭")
        w.set_family_name_when_add()
        if w.exec():
            with FamilyDB() as db:
                get_InputParishionerMessageinfo = w.get_InputFamilyMessageinfo()
                get_InputParishionerMessageinfo["family_school_id"] = self.login_info["parish_id"]
                get_InputParishionerMessageinfo["operator"] = self.login_info["user_name"]
                if self.login_info["user_type"] != 0:
                    get_InputParishionerMessageinfo["opera_type"] = 0
                else:
                    get_InputParishionerMessageinfo["opera_type"] = 2
                get_InputParishionerMessageinfo["opera_time"] = int(time.time())
                db.add_family(get_InputParishionerMessageinfo)
            self.load_family()

    def validate(self):
        """ 重写验证表单数据的方法 """
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=1000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return False
        return True  # 返回验证结果，True 表示验证通过，False 表示验证失败

    def get_InputParishionerMessageinfo(self):
        parishioner_messageinfo = {
            "student_name": self.Parishioner_Info_Edit_widgets.inputLine_1.text(),
            "student_gender": self.Parishioner_Info_Edit_widgets.inputLine_9.currentData(),
            "student_phonenum": self.Parishioner_Info_Edit_widgets.inputLine_3.text(),  # 性别字段与对应的下拉框
            "student_holyname": self.Parishioner_Info_Edit_widgets.inputLine_2.text(),  # 班级字段与对应的下拉框
            "student_family_id": self.Parishioner_Info_Edit_widgets.inputLine_11.currentData(),  # 语文字段与对应的输入框
            "student_identity_num": self.Parishioner_Info_Edit_widgets.inputLine_4.text(),  # 语文字段与对应的输入框
            "student_birthday": qdate_to_timestamp(self.Parishioner_Info_Edit_widgets.inputLine_10.getDate()),
            "student_note": self.Parishioner_Info_Edit_widgets.inputLine_13.text(),
            "operator": None,
            "opera_time": None,
            "opera_type": None,
            "student_school_id": None
        }
        return parishioner_messageinfo

    def set_InputParishionerMessageinfo(self, parishioner_messageinfo):
        self.Parishioner_Info_Edit_widgets.inputLine_1.setText(parishioner_messageinfo["student_name"])
        self.Parishioner_Info_Edit_widgets.inputLine_9.setCurrentIndex(parishioner_messageinfo["student_gender"])
        self.Parishioner_Info_Edit_widgets.inputLine_3.setText(parishioner_messageinfo["student_phonenum"])
        self.Parishioner_Info_Edit_widgets.inputLine_2.setText(parishioner_messageinfo["student_holyname"])
        self.Parishioner_Info_Edit_widgets.inputLine_4.setText(str(parishioner_messageinfo["student_identity_num"]))
        self.Parishioner_Info_Edit_widgets.inputLine_10.setDate(
            timestamp_to_date(parishioner_messageinfo["student_birthday"]))
        self.Parishioner_Info_Edit_widgets.inputLine_13.setText(parishioner_messageinfo["student_note"])
        family_idx = self.Parishioner_Info_Edit_widgets.inputLine_11.findData(
            parishioner_messageinfo["student_family_id"])
        self.Parishioner_Info_Edit_widgets.inputLine_11.setCurrentIndex(family_idx)
        if self.login_info["user_type"] == 1 and parishioner_messageinfo["opera_type"] != 0:
            self.Parishioner_Info_Edit_widgets.inputLine_1.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_2.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_3.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_4.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_9.setDisabled(True)
            self.Parishioner_Info_Edit_widgets.inputLine_10.setDisabled(True)
            self.Parishioner_Info_Edit_widgets.inputLine_11.setDisabled(True)
            self.Parishioner_Info_Edit_widgets.inputLine_13.setReadOnly(True)

            self.readOnly_flag = True
            exec_log = "非录入状态下仅支持查看"
            InfoBar.warning(title="警告", content=exec_log, parent=self,
                            duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
        elif self.login_info["user_type"] == 2:
            self.Parishioner_Info_Edit_widgets.inputLine_1.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_2.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_3.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_4.setReadOnly(True)
            self.Parishioner_Info_Edit_widgets.inputLine_9.setDisabled(True)
            self.Parishioner_Info_Edit_widgets.inputLine_10.setDisabled(True)
            self.Parishioner_Info_Edit_widgets.inputLine_11.setDisabled(True)
            self.Parishioner_Info_Edit_widgets.inputLine_13.setReadOnly(True)
            self.readOnly_flag = True
            exec_log = "游客仅支持查看"
            InfoBar.warning(title="警告", content=exec_log, parent=self,
                            duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
        return

    def load_family(self):
        self.Parishioner_Info_Edit_widgets.inputLine_11.clear()  # 清空 classCombo 下拉框中的所有选项
        with FamilyDB() as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            self.family_info = db.fetch_family_with_school_id(
                self.login_info["parish_id"])  # 如果没有可管理的班级 ID 列表，则获取所有班级信息
        self.Parishioner_Info_Edit_widgets.inputLine_11.addItem('请选择班级',
                                                                None)  # 在下拉框中添加默认选项 "请选择班级"，并将其关联的数据设为 None

        for family_info in self.family_info:  # 遍历获取到的班级信息列表
            self.Parishioner_Info_Edit_widgets.inputLine_11.addItem(family_info['family_name'],
                                                                    userData=family_info['family_id'])


class Parishioner_Main_Interface(QWidget):
    def __init__(self, login_info, ObjectName):
        super().__init__()
        self.login_info = login_info
        # 创建主布局
        self.setObjectName(ObjectName)
        self.parishioner_info_all = None
        self.cur_parish_id = self.login_info['parish_id']
        main_layout = QVBoxLayout(self)
        self.setMinimumSize(500, 500)

        self.BaseMainInterface = BaseMainInterface(self)
        self.BaseMainInterface.label.setMinimumSize(100, 100)

        pixmap = QPixmap("./resource/pic/1.png").scaled(
            self.BaseMainInterface.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.label.setPixmap(pixmap)
        self.BaseMainInterface.label_2.setText("添加人员")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        self.BaseMainInterface.BaseQuery.addButton.clicked.connect(self.add_parishioner)
        self.BaseMainInterface.BaseQuery.delButton.clicked.connect(self.delete_parishioner)
        self.BaseMainInterface.BaseQuery.ModButton.clicked.connect(self.modify_parishioner)
        self.BaseMainInterface.BaseQuery.searchInput.searchSignal.connect(self.query_parishioner_info_with_like)
        self.BaseMainInterface.BaseQuery.searchInput.returnPressed.connect(self.query_parishioner_info_with_like)
        self.BaseMainInterface.BaseQuery.ReviewButton.clicked.connect(self.review_data)

        if self.login_info["user_type"] == 0:
            self.parishioner_tableView_header = [
                "姓名", "圣名", "性别", "手机", "家庭名称", "生日", "备注", "操作人员", "操作时间", "状态", "归档"
            ]
            self.header_info = [
                'student_name', 'student_holyname', 'student_gender',
                'student_phonenum', 'family_name', 'student_birthday',
                'student_note', 'operator', 'opera_time', 'opera_type'
            ]
        else:
            self.BaseMainInterface.BaseQuery.ReviewButton.setText("提交审阅")
            self.parishioner_tableView_header = [
                "姓名", "圣名", "性别", "手机", "家庭名称", "生日", "备注", "状态", "提交审阅"
            ]
            self.header_info = [
                'student_name', 'student_holyname', 'student_gender',
                'student_phonenum', 'family_name', 'student_birthday',
                'student_note', 'opera_type'
            ]
        self.BaseMainInterface.BaseQuery.tableWidget.setColumnCount(len(self.parishioner_tableView_header))
        self.BaseMainInterface.BaseQuery.tableWidget.setHorizontalHeaderLabels(self.parishioner_tableView_header)
        header = self.BaseMainInterface.BaseQuery.tableWidget.horizontalHeader()
        header.resizeSection(0, 50)
        header.resizeSection(1, 50)
        header.resizeSection(3, 50)
        header.resizeSection(4, 100)
        # 其他列自适应宽度
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)

    def query_parishioner_info_with_like(self):
        if self.BaseMainInterface.BaseQuery.searchInput.text() == "":
            self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
        else:
            self.Load_Parishioner(QUERY_TYPE.QUERY_LIKE, self.cur_parish_id,
                                  self.BaseMainInterface.BaseQuery.searchInput.text())

    def Load_Parishioner(self, query_type, school_id, query_param=None):
        with StudentDB() as db:
            if query_type == QUERY_TYPE.QUERY_ALL:
                self.parishioner_info_all = db.fetch_students_with_school_id(school_id)
            elif query_type == QUERY_TYPE.QUERY_LIKE:
                self.parishioner_info_all = db.fetch_students_with_like(school_id, query_param)
            else:
                return

        if self.parishioner_info_all is None:
            return

        self.BaseMainInterface.BaseQuery.set_viewWidget_data(self.header_info, self.parishioner_info_all)

    def review_data(self):
        if self.login_info["user_type"] == 0:
            opera_type = 2
        else:
            opera_type = 1
        update_flag = False
        with StudentDB() as db:
            for idx in range(self.BaseMainInterface.BaseQuery.tableWidget.rowCount()):
                if self.BaseMainInterface.BaseQuery.tableWidget.cellWidget(idx, len(self.header_info)).isChecked():
                    family_info = self.parishioner_info_all[idx]
                    db.set_data_opera_type(family_info["student_id"], opera_type)
                    update_flag = True
        if update_flag:
            self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
    @check_auth_permission(required_permission={"module_data": "parishioner", "permission_data": "add"})
    def add_parishioner(self):
        w = Parishioner_MessageBox(self.login_info, self)
        w.titleLabel.setText("添加人员")
        if w.exec():
            with StudentDB() as db:
                get_InputParishionerMessageinfo = w.get_InputParishionerMessageinfo()
                get_InputParishionerMessageinfo["student_school_id"] = self.cur_parish_id
                get_InputParishionerMessageinfo["operator"] = self.login_info["user_name"]
                get_InputParishionerMessageinfo["opera_time"] = int(time.time())
                if self.login_info["user_type"] != 0:
                    get_InputParishionerMessageinfo["opera_type"] = 0
                else:
                    get_InputParishionerMessageinfo["opera_type"] = 2
                db.add_student(get_InputParishionerMessageinfo)
            self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
            return True
        return False

    @check_auth_permission(required_permission={"module_data": "parishioner", "permission_data": "delete"})
    def delete_parishioner(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            if self.login_info["user_type"] != 0 and self.parishioner_info_all[idx]["opera_type"] > 0:
                exec_log = "审阅或归档模式下禁止删除数据"
                InfoBar.error(title="错误", content=exec_log, parent=self,
                                duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
                return False
            w = Parishioner_MessageBox(self.login_info, self)
            w.titleLabel.setText("删除人员")
            w.set_InputParishionerMessageinfo(self.parishioner_info_all[idx])
            if w.exec():
                with StudentDB() as db:
                    db.delete_student(self.parishioner_info_all[idx]["student_id"])
                self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
                return True
            return False

    @check_auth_permission(required_permission={"module_data": "parishioner", "permission_data": "modify"})
    def modify_parishioner(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = Parishioner_MessageBox(self.login_info, self)
            w.titleLabel.setText("修改人员信息")
            w.set_InputParishionerMessageinfo(self.parishioner_info_all[idx])
            if w.exec():
                if w.readOnly_flag is True:
                    return False
                with StudentDB() as db:
                    if w.set_reject_flag is True and self.login_info["user_type"] == 0:
                        db.set_data_opera_type(self.parishioner_info_all[idx]["student_id"], 0)
                        return True
                    parishioner_info = w.get_InputParishionerMessageinfo()
                    parishioner_info["student_id"] = self.parishioner_info_all[idx]["student_id"]
                    parishioner_info["student_school_id"] = self.cur_parish_id
                    parishioner_info["operator"] = self.login_info["user_name"]
                    parishioner_info["opera_time"] = int(time.time())
                    db.update_student(parishioner_info)
                self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
                return True
            return False

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login_info_1 = {
        "parish_id": 1,
        "parish_name": "崇义教区",
        "user_id": 1,
        "user_name": "admin",
        "user_type": 1,
        "user_authnum": 32767
    }
    main_window = Parishioner_Main_Interface(login_info_1, 'testParishioner_Main_Interface')
    main_window.resize(1000, 800)
    main_window.show()


    sys.exit(app.exec())
