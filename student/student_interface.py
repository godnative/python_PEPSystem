import enum
import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QCheckBox, QTableWidgetItem

from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from student.family_dialog import AddFamilyDialog
from student.stduent_basetemp import BaseStudentFuncTemp
from student.student_dialog import AddStudentDialog


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class StudentInterface(QWidget):
    def __init__(self, curSchool):
        super().__init__()
        self.verticalLayout = None
        self.curSchool = curSchool
        self.familys = None
        self.setObjectName("StudentInterface")
        self.baseStudentFuncTemp_1 = BaseStudentFuncTemp()
        self.baseStudentFuncTemp_2 = BaseStudentFuncTemp()
        self.student_viewTable_header_info = [
            "", "姓名", "性别", "手机", "家庭名称"
        ]
        self.family_viewTable_header_info = [
            "", "家庭名称", "地址", "备注"
        ]
        self.students = []
        self.setup_ui()
        self.load_student_data(QUERY_TYPE.QUERY_ALL, -1)
        self.load_family_data(QUERY_TYPE.QUERY_ALL, -1)

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_1.main_verticalLayout)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_2.main_verticalLayout)

        self.baseStudentFuncTemp_1.button_3.clicked.connect(self.query_family_info)
        self.baseStudentFuncTemp_2.button_3.clicked.connect(self.query_student_info)
        self.baseStudentFuncTemp_1.tableWidget.setColumnCount(len(self.student_viewTable_header_info))
        self.baseStudentFuncTemp_1.tableWidget.setHorizontalHeaderLabels(self.student_viewTable_header_info)
        self.baseStudentFuncTemp_1.searchInput.searchSignal.connect(self.query_student_info_with_like)
        self.baseStudentFuncTemp_1.searchInput.returnPressed.connect(self.query_student_info_with_like)

        self.baseStudentFuncTemp_2.tableWidget.setColumnCount(len(self.family_viewTable_header_info))
        self.baseStudentFuncTemp_2.tableWidget.setHorizontalHeaderLabels(self.family_viewTable_header_info)
        self.baseStudentFuncTemp_2.searchInput.searchSignal.connect(self.query_family_info_with_like)
        self.baseStudentFuncTemp_2.searchInput.returnPressed.connect(self.query_family_info_with_like)

        self.baseStudentFuncTemp_1.button_1.clicked.connect(self.add_student_info)
        self.baseStudentFuncTemp_2.button_1.clicked.connect(self.add_family_info)

    def query_student_info_with_like(self):
        if self.baseStudentFuncTemp_1.searchInput.text() == "":
            self.load_student_data(QUERY_TYPE.QUERY_ALL, -1)
        else:
            self.load_student_data(QUERY_TYPE.QUERY_LIKE, self.baseStudentFuncTemp_1.searchInput.text())

    def query_family_info_with_like(self):
        if self.baseStudentFuncTemp_2.searchInput.text() == "":
            self.load_family_data(QUERY_TYPE.QUERY_ALL, -1)
        else:
            self.load_family_data(QUERY_TYPE.QUERY_LIKE, self.baseStudentFuncTemp_2.searchInput.text())

    def query_family_info(self):
        family_id = self.baseStudentFuncTemp_1.tableWidget.currentRow()
        if family_id == -1:
            return
        self.load_family_data(QUERY_TYPE.QUERY_ONE, family_id)

    def query_student_info(self):
        family_id = self.baseStudentFuncTemp_2.tableWidget.currentRow()
        if family_id == -1:
            return
        self.load_student_data(QUERY_TYPE.QUERY_ONE, family_id)

    def load_family_data(self, type, family_id):  # 定义 load_data 方法，用于加载学生数据
        with FamilyDB() as db:
            if type == QUERY_TYPE.QUERY_ONE and family_id != -1:
                self.familys = db.fetch_family_with_family_id(self.students[family_id]["student_family_id"])
            elif type == QUERY_TYPE.QUERY_ALL and family_id == -1:
                self.familys = db.fetch_family_with_school_id(self.curSchool["school_id"])
            elif type == QUERY_TYPE.QUERY_LIKE:
                self.familys = db.fetch_family_with_like(family_id)
            else:
                return

        if self.familys is None:
            return

        header_info = [
            'family_name', 'family_address', 'family_notes'
        ]
        self.set_viewWidget_data(self.baseStudentFuncTemp_2.tableWidget, header_info, self.familys)

    def load_student_data(self, type, family_id):
        with StudentDB() as db:
            if type == QUERY_TYPE.QUERY_ONE and family_id != -1:
                self.students = db.fetch_students_with_school_id_and_family_id(
                    self.students[family_id]["student_family_id"])
            elif type == QUERY_TYPE.QUERY_ALL and family_id == -1:
                self.students = db.fetch_students_with_school_id(self.curSchool["school_id"])
            elif type == QUERY_TYPE.QUERY_LIKE:
                self.students = db.fetch_students_with_like(family_id)
            else:
                return

        if self.students is None:
            return

        header_info = [
            'student_name', 'student_gender', 'student_phonenum', 'family_name'
        ]
        self.set_viewWidget_data(self.baseStudentFuncTemp_1.tableWidget, header_info, self.students)

    def add_student_info(self):
        w = AddStudentDialog(self)
        if w.exec():
            print(w.get_InputStudentDialoginfo())
            with StudentDB() as db:
                db.add_student(w.get_InputStudentDialoginfo())
            self.load_student_data(QUERY_TYPE.QUERY_ALL, -1)

    def add_family_info(self):
        w = AddFamilyDialog(self)
        if w.exec():
            print(w.get_InputFamilyDialoginfo())
            with FamilyDB() as db:
                db.add_family(w.get_InputFamilyDialoginfo())
            self.load_family_data(QUERY_TYPE.QUERY_ALL, -1)

    @staticmethod
    def set_viewWidget_data(tableWidget, header_info, datas):
        tableWidget.clearContents()
        tableWidget.setRowCount(len(datas))
        for row, data in enumerate(datas):
            checkBox = QCheckBox()
            tableWidget.setCellWidget(row, 0, checkBox)
            for column, key in enumerate(header_info):
                value = data.get(key, "")
                item = QTableWidgetItem(str(value))
                tableWidget.setItem(row, column + 1, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentInterface()
    window.show()
    sys.exit(app.exec())
