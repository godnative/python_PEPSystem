import enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHeaderView
from qfluentwidgets import MessageBoxBase, SubtitleLabel, InfoBar

from BaseWidgets.BaseModule import BaseMainInterface, BaseMessageBoxWidget, BaseQueryWidget
from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from user.User_Interface import check_auth_permission


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class Family_MessageBox(MessageBoxBase):

    def __init__(self, cur_parish, massage_type, parent=None):
        super().__init__(parent)
        self.family_info = None
        self.cur_parish = cur_parish
        self.massage_type = massage_type
        self.titleLabel = SubtitleLabel('人员', self)
        self.family_Info_Edit_widgets = BaseMessageBoxWidget(self)
        self.header_info = [
            'student_name', 'student_holyname', 'student_gender', 'student_phonenum', 'family_name'
        ]

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.family_Info_Edit_widgets)

        self.BaseQueryWidget = BaseQueryWidget(self)

        parishioner_tableView_header = [
            "姓名", "圣名", "性别", "手机", "家庭名称"
        ]
        self.BaseQueryWidget.tableWidget.setColumnCount(len(parishioner_tableView_header))
        self.BaseQueryWidget.tableWidget.setHorizontalHeaderLabels(parishioner_tableView_header)
        self.viewLayout.addWidget(self.BaseQueryWidget)

        # 设置UI
        self.family_Info_Edit_widgets.label_1.setText("家庭名称")
        self.family_Info_Edit_widgets.label_3.setText("地址")
        self.family_Info_Edit_widgets.label_13.setText("备注")

        self.family_Info_Edit_widgets.label_2.hide()
        self.family_Info_Edit_widgets.inputLine_2.hide()
        self.family_Info_Edit_widgets.label_4.hide()
        self.family_Info_Edit_widgets.inputLine_4.hide()
        self.family_Info_Edit_widgets.label_5.hide()
        self.family_Info_Edit_widgets.inputLine_5.hide()
        self.family_Info_Edit_widgets.label_6.hide()
        self.family_Info_Edit_widgets.inputLine_6.hide()
        self.family_Info_Edit_widgets.label_7.hide()
        self.family_Info_Edit_widgets.inputLine_7.hide()
        self.family_Info_Edit_widgets.label_8.hide()
        self.family_Info_Edit_widgets.inputLine_8.hide()
        self.family_Info_Edit_widgets.label_9.hide()
        self.family_Info_Edit_widgets.inputLine_9.hide()
        self.family_Info_Edit_widgets.label_10.hide()
        self.family_Info_Edit_widgets.inputLine_10.hide()
        self.family_Info_Edit_widgets.label_11.hide()
        self.family_Info_Edit_widgets.inputLine_11.hide()
        self.family_Info_Edit_widgets.label_12.hide()
        self.family_Info_Edit_widgets.inputLine_12.hide()

        self.BaseQueryWidget.addButton.hide()
        self.BaseQueryWidget.delButton.hide()
        self.BaseQueryWidget.ModButton.hide()
        self.BaseQueryWidget.searchInput.hide()

        self.family_Info_Edit_widgets.pic.setMaximumSize(100, 100)
        pixmap = QPixmap("./resource/pic/4.png").scaled(
            self.family_Info_Edit_widgets.pic.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.family_Info_Edit_widgets.pic.setPixmap(pixmap)

        self.widget.setMinimumWidth(350)
        self.family_Info_Edit_widgets.inputLine_1.setMinimumWidth(200)
        self.family_Info_Edit_widgets.inputLine_3.setMinimumWidth(200)

        with FamilyDB() as db:
            self.cur_family_cnt = db.get_family_cnt_with_parish_id(self.cur_parish["school_id"]) + 1

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.family_Info_Edit_widgets.inputLine_1.text().strip():
            errors.append("请输入家庭名称")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.family_Info_Edit_widgets.inputLine_3.text().strip():
            errors.append("请选择家庭地址")  # 验证学号是否填写，如果未填写，添加错误信息

        if not self.family_Info_Edit_widgets.inputLine_13.text().strip():
            errors.append("请输入备注")  # 验证班级是否选择，如果未选择班级，添加错误信息

        if self.massage_type == 1 and self.BaseQueryWidget.tableWidget.rowCount() != 0:
            errors.append(
                "当前家庭还有%d个成员，请先移除成员后再删除家庭" % self.BaseQueryWidget.tableWidget.rowCount())  # 验证班级是否选择，如果未选择班级，添加错误信息

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

    def get_InputFamilyMessageinfo(self):
        family_messageinfo = {
            "family_name": self.family_Info_Edit_widgets.inputLine_1.text(),
            "family_address": self.family_Info_Edit_widgets.inputLine_3.text(),  # 性别字段与对应的下拉框
            "family_notes": self.family_Info_Edit_widgets.inputLine_13.text(),  # 班级字段与对应的下拉框
            "family_school_id": None
        }
        return family_messageinfo

    def set_InputfFamilyMessageinfo(self, family_messageinfo):
        self.family_Info_Edit_widgets.inputLine_1.setText(family_messageinfo["family_name"])
        self.family_Info_Edit_widgets.inputLine_3.setText(family_messageinfo["family_address"])
        self.family_Info_Edit_widgets.inputLine_13.setText(family_messageinfo["family_notes"])
        return

    def set_family_name_when_add(self):
        family_name = "%s第%d号家庭" % (self.cur_parish["school_name"], self.cur_family_cnt)
        self.family_Info_Edit_widgets.inputLine_1.setText(family_name)
        self.BaseQueryWidget.hide()


class Family_Main_Interface(QWidget):
    def __init__(self, cur_parish, cur_user, ObjectName):
        super().__init__()

        # 创建主布局
        self.family_info_all = None
        self.cur_parish = cur_parish
        self.cur_user = cur_user
        self.setObjectName(ObjectName)
        self.parishioner_info_all = None
        self.cur_parish_id = self.cur_parish["school_id"]
        main_layout = QVBoxLayout(self)

        self.BaseMainInterface = BaseMainInterface(self)
        self.BaseMainInterface.label.setMinimumSize(100, 100)
        pixmap = QPixmap("./resource/pic/3.png").scaled(
            self.BaseMainInterface.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.label.setPixmap(pixmap)
        self.BaseMainInterface.label_2.setText("添加家庭")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        self.BaseMainInterface.BaseQuery.addButton.clicked.connect(self.add_family)
        self.BaseMainInterface.BaseQuery.delButton.clicked.connect(self.delete_family)
        self.BaseMainInterface.BaseQuery.ModButton.clicked.connect(self.modify_family)
        self.BaseMainInterface.BaseQuery.searchInput.searchSignal.connect(self.query_family_info_with_like)
        self.BaseMainInterface.BaseQuery.searchInput.returnPressed.connect(self.query_family_info_with_like)

        self.family_viewTable_header_info = [
            "家庭名称", "地址", "备注"
        ]
        self.BaseMainInterface.BaseQuery.tableWidget.setColumnCount(len(self.family_viewTable_header_info))
        self.BaseMainInterface.BaseQuery.tableWidget.setHorizontalHeaderLabels(self.family_viewTable_header_info)
        header = self.BaseMainInterface.BaseQuery.tableWidget.horizontalHeader()
        # 其他列自适应宽度
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.Load_family(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)

    def query_family_info_with_like(self):
        if self.BaseMainInterface.BaseQuery.searchInput.text() == "":
            self.Load_family(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
        else:
            self.Load_family(QUERY_TYPE.QUERY_LIKE, self.cur_parish_id,
                             self.BaseMainInterface.BaseQuery.searchInput.text())

    def Load_family(self, query_type, school_id, query_param=None):
        with FamilyDB() as db:
            if query_type == QUERY_TYPE.QUERY_ALL:
                self.family_info_all = db.fetch_family_with_school_id(school_id)
            elif query_type == QUERY_TYPE.QUERY_LIKE:
                self.family_info_all = db.fetch_family_with_like(school_id, query_param)
            else:
                return

        if self.family_info_all is None:
            return

        header_info = [
            'family_name', 'family_address', 'family_notes'
        ]
        self.BaseMainInterface.BaseQuery.set_viewWidget_data(header_info, self.family_info_all)

    @check_auth_permission(required_permission={"module_data": "family", "permission_data": "add"})
    def add_family(self):
        w = Family_MessageBox(self.cur_parish, 0, self)
        w.titleLabel.setText("添加家庭")
        w.set_family_name_when_add()
        if w.exec():
            with FamilyDB() as db:
                get_InputParishionerMessageinfo = w.get_InputFamilyMessageinfo()
                get_InputParishionerMessageinfo["family_school_id"] = self.cur_parish_id
                db.add_family(get_InputParishionerMessageinfo)
            self.Load_family(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
            return True
        return False

    @check_auth_permission(required_permission={"module_data": "family", "permission_data": "delete"})
    def delete_family(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = Family_MessageBox(self.cur_parish, 1, self)
            del_family_id = self.family_info_all[idx]["family_id"]
            w.titleLabel.setText("删除家庭")
            with StudentDB() as db:
                parishioner_info_all = db.fetch_students_with_school_id_and_family_id(del_family_id)
                if parishioner_info_all is not None:
                    w.BaseQueryWidget.set_viewWidget_data(w.header_info, parishioner_info_all)
            w.set_InputfFamilyMessageinfo(self.family_info_all[idx])
            if w.exec():
                with FamilyDB() as db:
                    db.delete_family(self.family_info_all[idx]["family_id"])
                self.Load_family(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
                return True
            return False

    @check_auth_permission(required_permission={"module_data": "family", "permission_data": "modify"})
    def modify_family(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = Family_MessageBox(self.cur_parish, 2, self)
            del_family_id = self.family_info_all[idx]["family_id"]
            w.titleLabel.setText("修改家庭")
            with StudentDB() as db:
                parishioner_info_all = db.fetch_students_with_school_id_and_family_id(del_family_id)
                if parishioner_info_all is not None:
                    w.BaseQueryWidget.set_viewWidget_data(w.header_info, parishioner_info_all)
            w.set_InputfFamilyMessageinfo(self.family_info_all[idx])
            if w.exec():
                with FamilyDB() as db:
                    family = w.get_InputFamilyMessageinfo()
                    family["family_id"] = self.family_info_all[idx]["family_id"]
                    family["family_school_id"] = self.cur_parish_id
                    db.update_family(family)
                self.Load_family(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
                return True
            return False
