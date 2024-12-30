import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QCheckBox, QTableWidgetItem

from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from student.family_dialog import AddFamilyDialog
from student.stduent_basetemp import BaseStudentFuncTemp
from student.student_dialog import AddStudentDialog


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
        self.load_student_data(-1)
        self.load_family_data(-1)

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_1.main_verticalLayout)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_2.main_verticalLayout)

        self.baseStudentFuncTemp_1.button_3.clicked.connect(self.query_family_info)
        self.baseStudentFuncTemp_2.button_3.clicked.connect(self.query_student_info)
        self.baseStudentFuncTemp_1.tableWidget.setColumnCount(len(self.student_viewTable_header_info))
        self.baseStudentFuncTemp_1.tableWidget.setHorizontalHeaderLabels(self.student_viewTable_header_info)

        self.baseStudentFuncTemp_2.tableWidget.setColumnCount(len(self.family_viewTable_header_info))
        self.baseStudentFuncTemp_2.tableWidget.setHorizontalHeaderLabels(self.family_viewTable_header_info)

        self.baseStudentFuncTemp_1.button_1.clicked.connect(self.add_student_info)
        self.baseStudentFuncTemp_2.button_1.clicked.connect(self.add_family_info)

    def query_family_info(self):
        family_id = self.baseStudentFuncTemp_1.tableWidget.currentRow()
        if family_id == -1:
            return
        self.load_family_data(family_id)

    def query_student_info(self):
        family_id = self.baseStudentFuncTemp_2.tableWidget.currentRow()
        if family_id == -1:
            return
        self.load_student_data(family_id)

    def add_student_info(self):
        w = AddStudentDialog(self)
        if w.exec():
            print(w.get_InputStudentDialoginfo())
            with StudentDB() as db:
                db.add_student(w.get_InputStudentDialoginfo())
            self.load_student_data(-1)

    def add_family_info(self):
        w = AddFamilyDialog(self)
        if w.exec():
            print(w.get_InputFamilyDialoginfo())
            with FamilyDB() as db:
                db.add_family(w.get_InputFamilyDialoginfo())
            self.load_family_data(-1)

    def load_student_data(self, family_id):  # 定义 load_data 方法，用于加载学生数据
        # 使用假数据替换数据库查询
        with StudentDB() as db:
            if family_id == -1:
                self.students = db.fetch_students_with_school_id(self.curSchool["school_id"])
            else:
                self.students = db.fetch_students_with_school_id_and_family_id(
                    self.students[family_id]["student_family_id"])
            if self.students is None:
                return
        self.baseStudentFuncTemp_1.tableWidget.clearContents()
        self.baseStudentFuncTemp_1.tableWidget.setRowCount(len(self.students))
        for row, student in enumerate(self.students):
            checkBox = QCheckBox()
            self.baseStudentFuncTemp_1.tableWidget.setCellWidget(row, 0, checkBox)

            for column, key in enumerate(['student_name', 'student_gender', 'student_phonenum', 'family_name']):
                value = student.get(key, "")
                item = QTableWidgetItem(str(value))
                self.baseStudentFuncTemp_1.tableWidget.setItem(row, column + 1, item)

    def load_family_data(self, family_id):  # 定义 load_data 方法，用于加载学生数据

        # 使用假数据替换数据库查询
        with FamilyDB() as db:
            if family_id == -1:
                self.familys = db.fetch_family_with_school_id(self.curSchool["school_id"])
            else:
                self.familys = db.fetch_family_with_family_id(self.students[family_id]["student_family_id"])

            if self.familys is None:
                return
        self.baseStudentFuncTemp_2.tableWidget.clearContents()
        self.baseStudentFuncTemp_2.tableWidget.setRowCount(len(self.familys))
        for row, family in enumerate(self.familys):
            checkBox = QCheckBox()
            self.baseStudentFuncTemp_2.tableWidget.setCellWidget(row, 0, checkBox)

            for column, key in enumerate(['family_name', 'family_address', 'family_notes']):
                value = family.get(key, "")
                item = QTableWidgetItem(str(value))
                self.baseStudentFuncTemp_2.tableWidget.setItem(row, column + 1, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentInterface()
    window.show()
    sys.exit(app.exec())
