import enum
import time

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QHeaderView
from qfluentwidgets import MessageBoxBase, SubtitleLabel, InfoBar, PushButton

from BaseWidgets.BaseModule import BaseMainInterface, BaseMessageBoxWidget
from DataBase.student_db import StudentDB
from Parishioner.Parishioner_Interface import Parishioner_MessageBox
from user.User_Interface import check_auth_permission

class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2

class Deceased_Parishioner_Main_Interface(QWidget):
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
        self.BaseMainInterface.label_2.setText("亡者安息")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        self.BaseMainInterface.BaseQuery.addButton.setText("登记死亡人员")
        self.BaseMainInterface.BaseQuery.delButton.setText("恢复错误登记信息")
        self.BaseMainInterface.BaseQuery.addButton.clicked.connect(self.add_parishioner)
        self.BaseMainInterface.BaseQuery.delButton.clicked.connect(self.delete_parishioner)
        self.BaseMainInterface.BaseQuery.ModButton.hide()
        self.BaseMainInterface.BaseQuery.searchInput.searchSignal.connect(self.query_parishioner_info_with_like)
        self.BaseMainInterface.BaseQuery.searchInput.returnPressed.connect(self.query_parishioner_info_with_like)
        self.BaseMainInterface.BaseQuery.ReviewButton.hide()

        self.parishioner_tableView_header = [
            "姓名", "圣名", "性别",
            "家庭名称", "生日", "死亡状态",
            "死亡日期", "  "
        ]
        self.header_info = [
            'student_name', 'student_holyname', 'student_gender',
            'family_name', 'student_birthday', 'student_alive_state',
            'student_death_anniversary'

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
        with StudentDB(self) as db:
            if query_type == QUERY_TYPE.QUERY_ALL:
                self.parishioner_info_all = db.fetch_students_with_school_id(school_id, False)
            elif query_type == QUERY_TYPE.QUERY_LIKE:
                self.parishioner_info_all = db.fetch_students_with_like(school_id, query_param)
            else:
                return

        if self.parishioner_info_all is None:
            return

        self.BaseMainInterface.BaseQuery.set_viewWidget_data(self.header_info, self.parishioner_info_all)

    @check_auth_permission(required_permission={"module_data": "dead", "permission_data": "add"})
    def add_parishioner(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = Parishioner_MessageBox(self.login_info, 1, self)
            w.titleLabel.setText("登记死亡人员")
            w.set_InputParishionerMessageinfo(self.parishioner_info_all[idx])
            if w.exec():
                with StudentDB(self) as db:
                    parishioner_info = w.get_InputParishionerMessageinfo()
                    parishioner_info["student_alive_state"] = 0
                    parishioner_info["student_id"] = self.parishioner_info_all[idx]["student_id"]
                    parishioner_info["operator"] = self.login_info["user_name"]
                    parishioner_info["opera_time"] = int(time.time())
                    db.update_student_alive_state(parishioner_info)
                self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
                return True
            return False

    @check_auth_permission(required_permission={"module_data": "dead", "permission_data": "delete"})
    def delete_parishioner(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            with StudentDB(self) as db:
                parishioner_messageinfo = {
                    "student_alive_state": 1,
                    "student_death_anniversary": None,
                    "operator": self.login_info["user_name"],
                    "opera_time": int(time.time()),
                    "student_id": self.parishioner_info_all[idx]["student_id"]
                }
                db.update_student_alive_state(parishioner_messageinfo)
            self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
            return True


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
    main_window = Deceased_Parishioner_Main_Interface(login_info_1, 'testParishioner_Main_Interface')
    main_window.resize(1000, 800)
    main_window.show()


    sys.exit(app.exec())
