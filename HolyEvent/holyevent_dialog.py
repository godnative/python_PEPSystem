import enum
import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QCheckBox, QTableWidgetItem

from DataBase.family_db import FamilyDB
from DataBase.holyevent_db import HolyEventDB
from DataBase.student_db import StudentDB
from student.family_dialog import AddFamilyDialog
from student.stduent_basetemp import BaseStudentFuncTemp
from student.student_dialog import AddStudentDialog


class HOLYEVENT_TYPE(enum.Enum):
    HOLYEVENT_BAPTISM = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class Holyevent_baptism_Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.even_info = None
        self.verticalLayout = None
        self.setObjectName("Holyevent_baptism_Interface")
        self.baseStudentFuncTemp_1 = BaseStudentFuncTemp()
        self.even_viewTable_header_info = [
            "", "人员", "圣名", "日期", "施行人", "见证人", "堂区", "备注"
        ]

        self.students = []
        self.setup_ui()
        self.load_baptism_even_data(HOLYEVENT_TYPE.HOLYEVENT_BAPTISM)

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_1.main_verticalLayout)

        self.baseStudentFuncTemp_1.tableWidget.setColumnCount(len(self.even_viewTable_header_info))
        self.baseStudentFuncTemp_1.tableWidget.setHorizontalHeaderLabels(self.even_viewTable_header_info)
        # self.baseStudentFuncTemp_1.searchInput.searchSignal.connect(self.query_student_info_with_like)
        # self.baseStudentFuncTemp_1.searchInput.returnPressed.connect(self.query_student_info_with_like)

        self.baseStudentFuncTemp_1.button_1.clicked.connect(self.add_baptism_even)

    def load_baptism_even_data(self, type):
        with HolyEventDB() as db:
            self.even_info = db.fetch_all_event_by_type(type)

        if self.even_info is None:
            return

        self.even_viewTable_header_info = [
            "", "人员", "圣名", "日期", "施行人", "见证人", "堂区", "备注"
        ]
        header_info = [
            'holyevent_p1_name', 'holyevent_p1_name', 'holyevent_date', 'holyevent_implementer',
            'holyevent_witness', 'holyevent_school_id', 'holyevent_note'
        ]
        self.set_viewWidget_data(self.baseStudentFuncTemp_1.tableWidget, header_info, self.even_info)

    def add_baptism_even(self):
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
