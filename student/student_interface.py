
import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication

from student.stduent_basetemp import Student_Widget, Family_Widget, QUERY_TYPE


class StudentInterface(QWidget):
    def __init__(self, curSchool):
        super().__init__()
        self.verticalLayout = None
        self.curSchool = curSchool
        self.familys = None
        self.setObjectName("StudentInterface")
        self.student_widget = Student_Widget(self.curSchool)
        self.family_widget = Family_Widget(self.curSchool)


        self.students = []
        self.setup_ui()


    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.student_widget)
        self.verticalLayout.addWidget(self.family_widget)

        self.student_widget.baseStudentFuncTemp_1.button_3.clicked.connect(self.query_family_info)
        self.family_widget.baseStudentFuncTemp_2.button_3.clicked.connect(self.query_student_info)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentInterface()
    window.show()
    sys.exit(app.exec())
