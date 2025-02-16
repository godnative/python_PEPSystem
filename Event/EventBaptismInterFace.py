import enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from qfluentwidgets import MessageBoxBase, SubtitleLabel, InfoBar

from BaseWidgets.BaseModule import BaseMainInterface, BaseMessageBoxWidget
from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from family.family_interface import Family_MessageBox


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class EventBaptism_MessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.family_info = None
        self.titleLabel = SubtitleLabel('人员', self)
        self.BaseMessageBoxWidget = BaseMessageBoxWidget(self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.BaseMessageBoxWidget)

        # 设置UI
        self.BaseMessageBoxWidget.label_1.setText("姓名")
        self.BaseMessageBoxWidget.label_2.setText("圣名")
        self.BaseMessageBoxWidget.label_3.setText("手机")
        self.BaseMessageBoxWidget.label_4.setText("身份证")
        self.BaseMessageBoxWidget.label_9.setText("性别")
        self.BaseMessageBoxWidget.label_10.setText("出生日期")
        self.BaseMessageBoxWidget.label_11.setText("家庭")
        self.BaseMessageBoxWidget.inputLine_12.setText("添加家庭")
        self.BaseMessageBoxWidget.label_13.setText("备注")

        self.BaseMessageBoxWidget.label_5.hide()
        self.BaseMessageBoxWidget.inputLine_5.hide()
        self.BaseMessageBoxWidget.label_6.hide()
        self.BaseMessageBoxWidget.inputLine_6.hide()
        self.BaseMessageBoxWidget.label_7.hide()
        self.BaseMessageBoxWidget.inputLine_7.hide()
        self.BaseMessageBoxWidget.label_8.hide()
        self.BaseMessageBoxWidget.inputLine_8.hide()
        # self.Parishioner_Info_Edit_widgets.label_12.hide()
        self.BaseMessageBoxWidget.label_12.setText("     ")

        self.BaseMessageBoxWidget.inputLine_9.addItem("男", userData=0)
        self.BaseMessageBoxWidget.inputLine_9.addItem("女", userData=1)

        self.BaseMessageBoxWidget.pic.setMaximumSize(100, 100)
        pixmap = QPixmap("./resource/pic/2.png").scaled(
            self.BaseMessageBoxWidget.pic.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMessageBoxWidget.pic.setPixmap(pixmap)

        self.widget.setMinimumWidth(350)
        self.BaseMessageBoxWidget.inputLine_12.clicked.connect(self.add_family)
        self.load_family()

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.BaseMessageBoxWidget.inputLine_1.text().strip():
            errors.append("请输入姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if self.BaseMessageBoxWidget.inputLine_11.currentData() is None:
            errors.append("请选择家庭")  # 验证学号是否填写，如果未填写，添加错误信息

        if self.BaseMessageBoxWidget.inputLine_9.currentData() is None:
            errors.append("请选择性别")  # 验证班级是否选择，如果未选择班级，添加错误信息

        return errors  # 返回所有错误信息

    def add_family(self):
        school_info = {
            "school_id": 1,
            "school_name": "崇义小学"
        }
        w = Family_MessageBox(school_info, 0, self)
        w.titleLabel.setText("添加家庭")
        w.set_family_name_when_add()
        if w.exec():
            with FamilyDB() as db:
                get_InputParishionerMessageinfo = w.get_InputFamilyMessageinfo()
                get_InputParishionerMessageinfo["family_school_id"] = school_info["school_id"]
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
            "student_name": self.BaseMessageBoxWidget.inputLine_1.text(),
            "student_gender": self.BaseMessageBoxWidget.inputLine_9.currentData(),
            "student_phonenum": self.BaseMessageBoxWidget.inputLine_3.text(),  # 性别字段与对应的下拉框
            "student_holyname": self.BaseMessageBoxWidget.inputLine_2.text(),  # 班级字段与对应的下拉框
            "student_family_id": self.BaseMessageBoxWidget.inputLine_11.currentData(),  # 语文字段与对应的输入框
            "student_school_id": None
        }
        return parishioner_messageinfo

    def set_InputParishionerMessageinfo(self, parishioner_messageinfo):
        self.BaseMessageBoxWidget.inputLine_1.setText(parishioner_messageinfo["student_name"])
        self.BaseMessageBoxWidget.inputLine_9.setCurrentIndex(parishioner_messageinfo["student_gender"])
        self.BaseMessageBoxWidget.inputLine_3.setText(parishioner_messageinfo["student_phonenum"])
        self.BaseMessageBoxWidget.inputLine_2.setText(parishioner_messageinfo["student_holyname"])
        family_idx = self.BaseMessageBoxWidget.inputLine_11.findData(
            parishioner_messageinfo["student_family_id"])
        self.BaseMessageBoxWidget.inputLine_11.setCurrentIndex(family_idx)
        return

    def load_family(self):
        self.BaseMessageBoxWidget.inputLine_11.clear()  # 清空 classCombo 下拉框中的所有选项
        with FamilyDB() as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            self.family_info = db.fetch_family()  # 如果没有可管理的班级 ID 列表，则获取所有班级信息
        self.BaseMessageBoxWidget.inputLine_11.addItem('请选择班级',
                                                       None)  # 在下拉框中添加默认选项 "请选择班级"，并将其关联的数据设为 None

        for family_info in self.family_info:  # 遍历获取到的班级信息列表
            self.BaseMessageBoxWidget.inputLine_11.addItem(family_info['family_name'],
                                                           userData=family_info['family_id'])

    def set_lineedit_uneditable(self):  # 定义一个方法，用于设置输入框不可编辑
        self.BaseMessageBoxWidget.inputLine_1.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_2.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_3.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_4.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_9.setEnabled(False)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_10.setEnabled(False)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_11.setEnabled(False)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_12.hide()  # 设置输入框为只读模式，禁止用户输入


class Parishioner_Main_Interface(QWidget):
    def __init__(self, cur_parish_id=1):
        super().__init__()

        # 创建主布局
        self.setObjectName("Parishioner_Main_Interface")
        self.parishioner_info_all = None
        self.cur_parish_id = cur_parish_id
        main_layout = QVBoxLayout(self)

        self.BaseMainInterface = BaseMainInterface(self)
        self.BaseMainInterface.label.setMinimumSize(100, 100)
        # self.BaseMainInterface.label.setText("Parishioner")
        pixmap = QPixmap("./resource/pic/1.png").scaled(
            self.BaseMainInterface.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.label.setPixmap(pixmap)
        self.BaseMainInterface.label_2.setText("添加人员")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        self.resize(800, 600)

        self.BaseMainInterface.BaseQuery.addButton.clicked.connect(self.add_parishioner)
        self.BaseMainInterface.BaseQuery.delButton.clicked.connect(self.delete_parishioner)
        self.BaseMainInterface.BaseQuery.ModButton.clicked.connect(self.modify_parishioner)
        self.BaseMainInterface.BaseQuery.searchInput.searchSignal.connect(self.query_parishioner_info_with_like)
        self.BaseMainInterface.BaseQuery.searchInput.returnPressed.connect(self.query_parishioner_info_with_like)

        self.parishioner_tableView_header = [
             "姓名", "圣名", "性别", "手机", "家庭名称"
        ]
        self.BaseMainInterface.BaseQuery.tableWidget.setColumnCount(len(self.parishioner_tableView_header))
        self.BaseMainInterface.BaseQuery.tableWidget.setHorizontalHeaderLabels(self.parishioner_tableView_header)
        self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)

    def query_parishioner_info_with_like(self):
        if self.BaseMainInterface.BaseQuery.searchInput.text() == "":
            self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)
        else:
            self.Load_Parishioner(QUERY_TYPE.QUERY_LIKE, self.BaseMainInterface.BaseQuery.searchInput.text())

    def Load_Parishioner(self, query_type, query_param):
        with StudentDB() as db:
            if query_type == QUERY_TYPE.QUERY_ONE:
                self.parishioner_info_all = db.fetch_students_with_school_id_and_family_id(query_param)
            elif query_type == QUERY_TYPE.QUERY_ALL:
                self.parishioner_info_all = db.fetch_students_with_school_id(query_param)
            elif query_type == QUERY_TYPE.QUERY_LIKE:
                self.parishioner_info_all = db.fetch_students_with_like(query_param)
            else:
                return

        if self.parishioner_info_all is None:
            return

        header_info = [
            'student_name', 'student_holyname', 'student_gender', 'student_phonenum', 'family_name'
        ]
        self.BaseMainInterface.BaseQuery.set_viewWidget_data(header_info, self.parishioner_info_all)

    def add_parishioner(self):
        w = Parishioner_MessageBox(self)
        w.titleLabel.setText("添加人员")
        if w.exec():
            with StudentDB() as db:
                get_InputParishionerMessageinfo = w.get_InputParishionerMessageinfo()
                get_InputParishionerMessageinfo["student_school_id"] = self.cur_parish_id
                db.add_student(get_InputParishionerMessageinfo)
            self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)

    def delete_parishioner(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = Parishioner_MessageBox(self)
            w.titleLabel.setText("删除人员")
            w.set_lineedit_uneditable()
            w.set_InputParishionerMessageinfo(self.parishioner_info_all[idx])
            if w.exec():
                with StudentDB() as db:
                    db.delete_student(self.parishioner_info_all[idx]["student_id"])
                self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)

    def modify_parishioner(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = Parishioner_MessageBox(self)
            w.titleLabel.setText("修改人员信息")
            w.set_InputParishionerMessageinfo(self.parishioner_info_all[idx])
            if w.exec():
                with StudentDB() as db:
                    parishioner_info = w.get_InputParishionerMessageinfo()
                    parishioner_info["student_id"] = self.parishioner_info_all[idx]["student_id"]
                    parishioner_info["student_school_id"] = self.cur_parish_id
                    db.update_student(parishioner_info)
                self.Load_Parishioner(QUERY_TYPE.QUERY_ALL, self.cur_parish_id)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    main_window = Parishioner_Main_Interface()
    main_window.show()

    sys.exit(app.exec())
