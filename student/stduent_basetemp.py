# student/student_dialog.py文件中
import enum
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
    QHeaderView, QApplication, QAbstractItemView, QCheckBox, \
    QTableWidgetItem  # 导入 PyQt6 模块中的 QGridLayout，用于栅格布局
from qfluentwidgets import TableWidget, PushButton, CardWidget, setCustomStyleSheet, \
    SearchLineEdit  # 导入 qfluentwidgets 模块中的组件

from DataBase.family_db import FamilyDB
from DataBase.student_db import StudentDB
from student.family_dialog import AddFamilyDialog
from student.student_dialog import AddStudentDialog
from utils.custom_style import ADD_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE, UPDATE_BUTTON_STYLE


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class Self_SerchLineEdit(SearchLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Return:
            print("按下了回车键")
            print("搜索框内容：", self.text())
        else:
            super().keyPressEvent(e)


class BaseStudentFuncTemp(QWidget):  # 定义一个操作学生函数的基类
    def __init__(self):  # 初始化方法，接收弹窗标题和父窗口作为参数
        super().__init__()  # 调用父类的初始化方法，设置父窗口
        self.setup_ui()  # 调用界面设置方法，初始化弹窗界面

    def setup_ui(self):  # 定义设置用户界面的方法
        self.main_verticalLayout = QVBoxLayout()

        card_widget = CardWidget(self)

        self.button_layout = QHBoxLayout(card_widget)
        self.button_1 = PushButton('Add', self)
        setCustomStyleSheet(self.button_1, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)
        self.searchInput = SearchLineEdit(self)
        self.searchInput.setPlaceholderText('Search')
        self.searchInput.setFixedWidth(500)

        self.button_2 = PushButton('Delete', self)
        setCustomStyleSheet(self.button_2, BATCH_DELETE_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE)
        self.button_3 = PushButton('query', self)
        setCustomStyleSheet(self.button_3, UPDATE_BUTTON_STYLE, UPDATE_BUTTON_STYLE)

        self.button_layout.addWidget(self.button_1)
        self.button_layout.addWidget(self.searchInput)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.button_2)
        self.button_layout.addWidget(self.button_3)

        self.main_verticalLayout.addWidget(card_widget)

        self.tableWidget = TableWidget(self)
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.main_verticalLayout.addWidget(self.tableWidget)
        self.setStyleSheet('StudentInterface{background-color:white}')

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


class Student_Widget(QWidget):
    def __init__(self, curSchool):
        super().__init__()
        self.verticalLayout = None
        self.curSchool = curSchool
        self.familys = None
        self.setObjectName("Student_Widget")
        self.baseStudentFuncTemp_1 = BaseStudentFuncTemp()
        self.student_viewTable_header_info = [
            "", "姓名", "圣名", "性别", "手机", "家庭名称"
        ]
        self.students = []
        self.setup_ui()
        self.load_student_data(QUERY_TYPE.QUERY_ALL, self.curSchool["school_id"])

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_1.main_verticalLayout)

        self.baseStudentFuncTemp_1.tableWidget.setColumnCount(len(self.student_viewTable_header_info))
        self.baseStudentFuncTemp_1.tableWidget.setHorizontalHeaderLabels(self.student_viewTable_header_info)
        self.baseStudentFuncTemp_1.searchInput.searchSignal.connect(self.query_student_info_with_like)
        self.baseStudentFuncTemp_1.searchInput.returnPressed.connect(self.query_student_info_with_like)

        self.baseStudentFuncTemp_1.button_1.clicked.connect(self.add_student_info)

    def query_student_info_with_like(self):
        if self.baseStudentFuncTemp_1.searchInput.text() == "":
            self.load_student_data(QUERY_TYPE.QUERY_ALL, self.curSchool["school_id"])
        else:
            self.load_student_data(QUERY_TYPE.QUERY_LIKE, self.baseStudentFuncTemp_1.searchInput.text())

    def load_student_data(self, type, query_param):
        with StudentDB() as db:
            if type == QUERY_TYPE.QUERY_ONE:
                self.students = db.fetch_students_with_school_id_and_family_id(query_param)
            elif type == QUERY_TYPE.QUERY_ALL:
                self.students = db.fetch_students_with_school_id(query_param)
            elif type == QUERY_TYPE.QUERY_LIKE:
                self.students = db.fetch_students_with_like(query_param)
            else:
                return

        if self.students is None:
            return

        header_info = [
            'student_name', 'student_holyname', 'student_gender', 'student_phonenum', 'family_name'
        ]
        self.baseStudentFuncTemp_1.set_viewWidget_data(self.baseStudentFuncTemp_1.tableWidget, header_info,
                                                       self.students)

    def add_student_info(self):
        w = AddStudentDialog(self)
        if w.exec():
            print(w.get_InputStudentDialoginfo())
            with StudentDB() as db:
                db.add_student(w.get_InputStudentDialoginfo())
            self.load_student_data(QUERY_TYPE.QUERY_ALL, self.curSchool["school_id"])


class Family_Widget(QWidget):
    def __init__(self, curSchool):
        super().__init__()
        self.verticalLayout = None
        self.curSchool = curSchool
        self.familys = None
        self.setObjectName("Family_Widget")
        self.baseStudentFuncTemp_2 = BaseStudentFuncTemp()
        self.family_viewTable_header_info = [
            "", "家庭名称", "地址", "备注"
        ]
        self.setup_ui()
        self.load_family_data(QUERY_TYPE.QUERY_ALL, self.curSchool["school_id"])

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_2.main_verticalLayout)

        self.baseStudentFuncTemp_2.tableWidget.setColumnCount(len(self.family_viewTable_header_info))
        self.baseStudentFuncTemp_2.tableWidget.setHorizontalHeaderLabels(self.family_viewTable_header_info)
        self.baseStudentFuncTemp_2.searchInput.searchSignal.connect(self.query_family_info_with_like)
        self.baseStudentFuncTemp_2.searchInput.returnPressed.connect(self.query_family_info_with_like)

        self.baseStudentFuncTemp_2.button_1.clicked.connect(self.add_family_info)

    def query_family_info_with_like(self):
        if self.baseStudentFuncTemp_2.searchInput.text() == "":
            self.load_family_data(QUERY_TYPE.QUERY_ALL, self.curSchool["school_id"])
        else:
            self.load_family_data(QUERY_TYPE.QUERY_LIKE, self.baseStudentFuncTemp_2.searchInput.text())

    def load_family_data(self, type, query_param):  # 定义 load_data 方法，用于加载学生数据
        with FamilyDB() as db:
            if type == QUERY_TYPE.QUERY_ONE:
                self.familys = db.fetch_family_with_family_id(query_param)
            elif type == QUERY_TYPE.QUERY_ALL:
                self.familys = db.fetch_family_with_school_id(query_param)
            elif type == QUERY_TYPE.QUERY_LIKE:
                self.familys = db.fetch_family_with_like(query_param)
            else:
                return

        if self.familys is None:
            return

        header_info = [
            'family_name', 'family_address', 'family_notes'
        ]
        self.baseStudentFuncTemp_2.set_viewWidget_data(self.baseStudentFuncTemp_2.tableWidget, header_info,
                                                       self.familys)

    def add_family_info(self):
        w = AddFamilyDialog(self)
        if w.exec():
            print(w.get_InputFamilyDialoginfo())
            with FamilyDB() as db:
                db.add_family(w.get_InputFamilyDialoginfo())
            self.load_family_data(QUERY_TYPE.QUERY_ALL, self.curSchool["school_id"])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddStudentDialog()
    window.show()
    sys.exit(app.exec())
