from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication, QHeaderView, QCheckBox, QTableWidgetItem
from qfluentwidgets import CardWidget, PushButton, SearchLineEdit, TableWidget, setCustomStyleSheet

from student.student_dialog import AddStudentDialog
from utils.custom_style import ADD_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE
from DataBase.student_db import StudentDB
import sys


class StudentInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("StudentInterface")
        self.students = []
        self.setup_ui()
        self.load_data()
        self.populate_table()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        card_widget = CardWidget(self)

        button_layout = QHBoxLayout(card_widget)
        self.addButton = PushButton('Add',self)
        setCustomStyleSheet(self.addButton, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)
        self.addButton.clicked.connect(self.addStudentInfo)
        self.searchInput = SearchLineEdit(self)
        self.searchInput.setPlaceholderText('Search')
        self.searchInput.setFixedWidth(500)
        self.batchDeleteButton = PushButton('Delete',self)
        setCustomStyleSheet(self.batchDeleteButton, BATCH_DELETE_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE)

        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.searchInput)
        button_layout.addStretch(1)
        button_layout.addWidget(self.batchDeleteButton)

        layout.addWidget(card_widget)

        self.tableWidget = TableWidget(self)
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setWordWrap(False)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(
            ["", "学生ID", "姓名", "学号", "性别", "班级", "语文", "数学", "英语", "总分", "操作"])

        layout.addWidget(self.tableWidget)
        self.setStyleSheet('StudentInterface{background-color:white}')
        self.resize(1280,720)

    def addStudentInfo(self):
        w = AddStudentDialog(self)
        if w.exec():
            print(w.get_InputStudentDialoginfo())
            with StudentDB() as db:
                db.add_student(w.get_InputStudentDialoginfo())
            self.load_data()
            self.populate_table()

    def load_data(self):  # 定义 load_data 方法，用于加载学生数据
        # 使用假数据替换数据库查询
        with StudentDB() as db:
            self.students = db.fetch_students()

    def populate_table(self):
        self.tableWidget.setRowCount(len(self.students))
        for row, student in enumerate(self.students):
            self.setup_table_row(row, student)

    def setup_table_row(self, row, student):
        checkBox = QCheckBox()
        self.tableWidget.setCellWidget(row, 0, checkBox)

        for column, key in enumerate(['student_id', 'student_name', 'student_number', 'gender', 'class_name', 'chinese_score', 'math_score',
                 'english_score', 'total_score']):
            value = student.get(key,"")
            item = QTableWidgetItem(str(value))
            self.tableWidget.setItem(row, column + 1, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentInterface()
    window.show()
    sys.exit(app.exec())