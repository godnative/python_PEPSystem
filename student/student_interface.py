import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QCheckBox, QTableWidgetItem

from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from student.family_dialog import AddFamilyDialog
from student.stduent_basetemp import BaseStudentFuncTemp
from student.student_dialog import AddStudentDialog


class StudentInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.verticalLayout = None
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
        self.load_student_data()
        self.load_family_data()

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_1.main_verticalLayout)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_2.main_verticalLayout)

        self.baseStudentFuncTemp_1.tableWidget.setColumnCount(len(self.student_viewTable_header_info))
        self.baseStudentFuncTemp_1.tableWidget.setHorizontalHeaderLabels(self.student_viewTable_header_info)

        self.baseStudentFuncTemp_2.tableWidget.setColumnCount(len(self.family_viewTable_header_info))
        self.baseStudentFuncTemp_2.tableWidget.setHorizontalHeaderLabels(self.family_viewTable_header_info)

        self.baseStudentFuncTemp_1.button_1.clicked.connect(self.add_student_info)
        self.baseStudentFuncTemp_2.button_1.clicked.connect(self.add_family_info)

    def add_student_info(self):
        w = AddStudentDialog(self)
        if w.exec():
            print(w.get_InputStudentDialoginfo())
            with StudentDB() as db:
                db.add_student(w.get_InputStudentDialoginfo())
            self.load_student_data()

    def add_family_info(self):
        w = AddFamilyDialog(self)
        if w.exec():
            print(w.get_InputFamilyDialoginfo())
            with FamilyDB() as db:
                db.add_family(w.get_InputFamilyDialoginfo())
            self.load_family_data()

    def load_student_data(self):  # 定义 load_data 方法，用于加载学生数据
        # 使用假数据替换数据库查询
        with StudentDB() as db:
            self.students = db.fetch_students()

        self.baseStudentFuncTemp_1.tableWidget.setRowCount(len(self.students))
        for row, student in enumerate(self.students):
            checkBox = QCheckBox()
            self.baseStudentFuncTemp_1.tableWidget.setCellWidget(row, 0, checkBox)

            for column, key in enumerate(['student_name', 'student_gender', 'student_phonenum', 'family_name']):
                value = student.get(key, "")
                item = QTableWidgetItem(str(value))
                self.baseStudentFuncTemp_1.tableWidget.setItem(row, column + 1, item)

    def load_family_data(self):  # 定义 load_data 方法，用于加载学生数据
        # 使用假数据替换数据库查询
        with FamilyDB() as db:
            self.familys = db.fetch_family()

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
