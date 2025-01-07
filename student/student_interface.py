import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication
from qfluentwidgets import InfoBar

from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from student.family_dialog import AddFamilyDialog, ModifyFamilyDialog, DelFamilyDialog
from student.stduent_basetemp import Student_Widget, Family_Widget, QUERY_TYPE
from student.student_dialog import AddStudentDialog, ModifyStudentDialog, DelStudentDialog


class StudentInterface(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.verticalLayout = None
        self.role = parent.role
        self.school_info = parent.school_info
        self.familys = None
        self.setObjectName("StudentInterface")
        self.student_widget = Student_Widget(self)
        self.family_widget = Family_Widget(self)

        self.setup_ui()

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.student_widget)
        self.verticalLayout.addWidget(self.family_widget)

        self.student_widget.baseStudentFuncTemp_1.button_4.clicked.connect(self.query_family_info)
        self.family_widget.baseStudentFuncTemp_2.button_4.clicked.connect(self.query_student_info)

        self.student_widget.baseStudentFuncTemp_1.button_1.clicked.connect(self.add_student_info)
        self.student_widget.baseStudentFuncTemp_1.button_2.clicked.connect(self.modify_student_info)
        self.student_widget.baseStudentFuncTemp_1.button_3.clicked.connect(self.del_student_info)

        self.family_widget.baseStudentFuncTemp_2.button_1.clicked.connect(self.add_family_info)
        self.family_widget.baseStudentFuncTemp_2.button_2.clicked.connect(self.modify_family_info)
        self.family_widget.baseStudentFuncTemp_2.button_3.clicked.connect(self.del_family_info)

    def query_family_info(self):
        idx = self.student_widget.baseStudentFuncTemp_1.tableWidget.currentRow()
        if idx == -1:
            return
        self.family_widget.load_family_data(QUERY_TYPE.QUERY_ONE,
                                            self.student_widget.students[idx]["student_family_id"])

    def query_student_info(self):
        idx = self.family_widget.baseStudentFuncTemp_2.tableWidget.currentRow()
        if idx == -1:
            return
        self.student_widget.load_student_data(QUERY_TYPE.QUERY_ONE, self.family_widget.familys[idx]["family_id"])

    def add_student_info(self):
        w = AddStudentDialog(self)
        if w.exec():
            with StudentDB() as db:
                db.add_student(w.get_InputStudentDialoginfo())
            self.student_widget.load_student_data(QUERY_TYPE.QUERY_ALL, self.school_info["school_id"])

    def modify_student_info(self):
        idx = self.student_widget.baseStudentFuncTemp_1.tableWidget.currentRow()
        if idx != -1:
            w = ModifyStudentDialog(self)
            w.set_InputStudentDialoginfo(self.student_widget.students[idx])
            if w.exec():
                with StudentDB() as db:
                    student = w.get_InputStudentDialoginfo()
                    student["student_id"] = self.student_widget.students[idx]["student_id"]
                    db.update_student(student)
                self.student_widget.load_student_data(QUERY_TYPE.QUERY_ALL, self.school_info["school_id"])

    def del_student_info(self):
        idx = self.student_widget.baseStudentFuncTemp_1.tableWidget.currentRow()
        if idx != -1:
            w = DelStudentDialog(self)
            w.set_InputStudentDialoginfo(self.student_widget.students[idx])
            if w.exec():
                with StudentDB() as db:
                    db.delete_student(self.student_widget.students[idx]["student_id"])
                self.student_widget.load_student_data(QUERY_TYPE.QUERY_ALL, self.school_info["school_id"])

    def add_family_info(self):
        w = AddFamilyDialog(self)
        if w.exec():
            print(w.get_InputFamilyDialoginfo())
            with FamilyDB() as db:
                db.add_family(w.get_InputFamilyDialoginfo())
            self.family_widget.load_family_data(QUERY_TYPE.QUERY_ALL, self.school_info["school_id"])

    def modify_family_info(self):
        idx = self.family_widget.baseStudentFuncTemp_2.tableWidget.currentRow()
        if idx != -1:
            w = ModifyFamilyDialog(self)
            w.set_InputFamilyDialoginfo(self.family_widget.familys[idx])
            if w.exec():
                with FamilyDB() as db:
                    family = w.get_InputFamilyDialoginfo()
                    family["family_id"] = self.family_widget.familys[idx]["family_id"]
                    db.update_family(family)
                self.family_widget.load_family_data(QUERY_TYPE.QUERY_ALL, self.school_info["school_id"])

    def del_family_info(self):
        idx = self.family_widget.baseStudentFuncTemp_2.tableWidget.currentRow()
        if idx != -1:
            w = DelFamilyDialog(self)
            w.set_InputFamilyDialoginfo(self.family_widget.familys[idx])
            if w.exec():
                with StudentDB() as db:
                    studentcnt = len(
                        db.fetch_students_with_school_id_and_family_id(self.family_widget.familys[idx]["family_id"]))
                    if studentcnt == 0:
                        with FamilyDB() as familydb:
                            familydb.delete_family(self.family_widget.familys[idx]["family_id"])
                            self.family_widget.load_family_data(QUERY_TYPE.QUERY_ALL, self.school_info["school_id"])
                    else:
                        errors = "家庭：%s \n还有 %d 个成员\n请先移除或删除后再操作" % (
                        self.family_widget.familys[idx]["family_name"], studentcnt)
                        InfoBar.error(title="输入有误", content=errors, parent=self,
                                      duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentInterface()
    window.show()
    sys.exit(app.exec())
