import enum
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QLabel, QAbstractItemView, QHeaderView, \
    QCheckBox, QTableWidgetItem
from qfluentwidgets import LineEdit, InfoBar, PushButton, TableWidget, \
    SearchLineEdit

from DataBase.family_db import FamilyDB
from DataBase.holyevent_db import HolyEventDB
from DataBase.student_db import StudentDB
from student.stduent_basetemp import QUERY_TYPE


class HOLY_EVENT_TYPE(enum.Enum):
    HOLY_EVENT_BAPTISM = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class BaseEvenFuncTemp(QWidget):  # 定义一个操作学生函数的基类
    def __init__(self):  # 初始化方法，接收弹窗标题和父窗口作为参数
        super().__init__()  # 调用父类的初始化方法，设置父窗口
        self.setup_ui()  # 调用界面设置方法，初始化弹窗界面

    def setup_ui(self):  # 定义设置用户界面的方法
        self.main_verticalLayout = QVBoxLayout()
        self.main_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7 = QHBoxLayout()
        self.label_1 = QLabel()

        self.horizontalLayout_7.addWidget(self.label_1)

        self.verticalLayout_2 = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        self.label_2 = QLabel()

        self.horizontalLayout.addWidget(self.label_2)

        self.lineEdit_1 = LineEdit()

        self.horizontalLayout.addWidget(self.lineEdit_1)

        self.label_3 = QLabel()

        self.horizontalLayout.addWidget(self.label_3)

        self.lineEdit_2 = LineEdit()

        self.horizontalLayout.addWidget(self.lineEdit_2)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.label_4 = QLabel()

        self.horizontalLayout_2.addWidget(self.label_4)

        self.lineEdit_3 = LineEdit()

        self.horizontalLayout_2.addWidget(self.lineEdit_3)

        self.label_5 = QLabel()

        self.horizontalLayout_2.addWidget(self.label_5)

        self.lineEdit_4 = LineEdit()

        self.horizontalLayout_2.addWidget(self.lineEdit_4)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.label_6 = QLabel()

        self.horizontalLayout_3.addWidget(self.label_6)

        self.lineEdit_5 = LineEdit()

        self.horizontalLayout_3.addWidget(self.lineEdit_5)

        self.label_7 = QLabel()

        self.horizontalLayout_3.addWidget(self.label_7)

        self.lineEdit_6 = LineEdit()

        self.horizontalLayout_3.addWidget(self.lineEdit_6)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.label_8 = QLabel()

        self.horizontalLayout_4.addWidget(self.label_8)

        self.lineEdit_7 = LineEdit()

        self.horizontalLayout_4.addWidget(self.lineEdit_7)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.pushButton_1 = PushButton()

        self.horizontalLayout_5.addWidget(self.pushButton_1)

        self.pushButton_2 = PushButton()

        self.horizontalLayout_5.addWidget(self.pushButton_2)

        self.pushButton_3 = PushButton()

        self.horizontalLayout_5.addWidget(self.pushButton_3)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.main_verticalLayout.addLayout(self.horizontalLayout_7)

        self.verticalLayout = QVBoxLayout()

        self.horizontalLayout_6 = QHBoxLayout()

        self.pushButton_4 = PushButton()

        self.horizontalLayout_6.addWidget(self.pushButton_4)

        self.searchInput = SearchLineEdit(self)
        self.searchInput.setPlaceholderText('Search')
        self.searchInput.setFixedWidth(500)

        self.horizontalLayout_6.addWidget(self.searchInput)

        self.pushButton_5 = PushButton()

        self.horizontalLayout_6.addWidget(self.pushButton_5)

        self.pushButton_6 = PushButton()

        self.horizontalLayout_6.addWidget(self.pushButton_6)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.tableWidget = TableWidget()
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.verticalLayout.addWidget(self.tableWidget)

        self.main_verticalLayout.addLayout(self.verticalLayout)

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


class HolyEventBaptismInterFace(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.even_info = None
        self.verticalLayout = None
        self.role = parent.role
        self.school_info = parent.school_info
        self.data_from_SQL = False
        self.person_info = None
        self.temp_family_id = 1
        self.evenType = 0
        # self.setObjectName("BaseHolyEventInterFace")
        self.baseStudentFuncTemp = BaseEvenFuncTemp()
        self.even_viewTable_header_info = [
            "", "姓名", "圣名", "施行人", "见证人", "堂区", "日期", "备注"
        ]
        self.even_database_header_info = [
            'holyevent_p1_name', 'holyevent_p1_holyname', 'holyevent_implementer',
            'holyevent_witness', 'holyevent_school_id', 'holyevent_date', 'holyevent_note'
        ]

        self.setup_ui()
        self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
        self.get_temp_family_id()

    def get_temp_family_id(self):
        with FamilyDB() as family_db:
            self.temp_family_id = family_db.fetch_tempfamily_with_school_id("临时", self.school_info["school_id"])
            if self.temp_family_id is None:
                self.temp_family_id = 1


    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp.main_verticalLayout)

        ##
        self.baseStudentFuncTemp.label_2.setText("姓名")
        self.baseStudentFuncTemp.label_3.setText("圣名")
        self.baseStudentFuncTemp.label_4.setText("施行人")
        self.baseStudentFuncTemp.label_5.setText("见证人")
        self.baseStudentFuncTemp.label_6.setText("堂区")
        self.baseStudentFuncTemp.label_7.setText("日期")
        self.baseStudentFuncTemp.label_8.setText("备注")
        self.baseStudentFuncTemp.pushButton_1.setText("添加")

        self.baseStudentFuncTemp.tableWidget.setColumnCount(len(self.even_viewTable_header_info))
        self.baseStudentFuncTemp.tableWidget.setHorizontalHeaderLabels(self.even_viewTable_header_info)
        self.baseStudentFuncTemp.searchInput.searchSignal.connect(self.query_even_info_with_like)
        self.baseStudentFuncTemp.searchInput.returnPressed.connect(self.query_even_info_with_like)

        self.baseStudentFuncTemp.pushButton_1.clicked.connect(self.add_even_info)

        self.baseStudentFuncTemp.label_1.setPixmap(QPixmap("./resource/pic/c1.png"))

    def query_even_info_with_like(self):
        if self.baseStudentFuncTemp.searchInput.text() == "":
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
        else:
            self.load_even_data(QUERY_TYPE.QUERY_LIKE, self.evenType, self.baseStudentFuncTemp.searchInput.text())

    def load_even_data(self, query_type, even_type, query_param):
        with HolyEventDB() as db:
            if QUERY_TYPE.QUERY_ALL == query_type:
                self.even_info = db.fetch_all_event_by_type(even_type)
            elif QUERY_TYPE.QUERY_LIKE == query_type:
                self.even_info = db.fetch_even_with_like(even_type, query_param)
            elif QUERY_TYPE.QUERY_ONE == query_type:
                self.even_info = db.fetch_all_event_by_type(even_type)

        if self.even_info is None:
            return

        self.baseStudentFuncTemp.set_viewWidget_data(self.baseStudentFuncTemp.tableWidget,
                                                     self.even_database_header_info, self.even_info)

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.baseStudentFuncTemp.lineEdit_1.text().strip():
            errors.append("请输入姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.baseStudentFuncTemp.lineEdit_2.text().strip():
            errors.append("请输入圣名")  # 验证学号是否填写，如果未填写，添加错误信息

        if not self.baseStudentFuncTemp.lineEdit_3.text().strip():
            errors.append("请输入施行人")  # 验证学号是否填写，如果未填写，添加错误信息

        return errors  # 返回所有错误信息

    def _get_even_info(self):
        even_info = {
            'holyevent_p1_name': self.baseStudentFuncTemp.lineEdit_1.text(),
            'holyevent_p1_holyname': self.baseStudentFuncTemp.lineEdit_2.text(),
            'holyevent_implementer': self.baseStudentFuncTemp.lineEdit_3.text(),
            'holyevent_witness': self.baseStudentFuncTemp.lineEdit_4.text(),
            'holyevent_school_id': self.baseStudentFuncTemp.lineEdit_5.text(),
            'holyevent_date': self.baseStudentFuncTemp.lineEdit_6.text(),
            'holyevent_note': self.baseStudentFuncTemp.lineEdit_7.text()
        }
        return even_info

    def add_even_info(self):
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        if self.data_from_SQL:
            # 如果是从数据库中找到的人员，就修改圣名即可
            with StudentDB() as db:
                even_info = self._get_even_info()
                db.update_student_holyname(self.person_info['student_id'], even_info['holyevent_p1_holyname'])
        else:
            # 如果是新建的人，就添加人物数据并添加到零时家庭中
            with StudentDB() as db:
                even_info = self._get_even_info()
                StudentInfo = {
                    "student_name": even_info['holyevent_p1_name'],
                    "student_gender": 0,
                    "student_phonenum": "",  # 性别字段与对应的下拉框
                    "student_holyname": even_info['holyevent_p1_holyname'],  # 班级字段与对应的下拉框
                    "student_family_id": self.temp_family_id,  # 语文字段与对应的输入框
                    "student_school_id": self.school_info["school_id"]  # 语文字段与对应的输入框
                }
                db.add_student(StudentInfo)
        with HolyEventDB() as db:
            even_info = self._get_even_info()
            even_info['holyevent_p1_id'] = self.person_info['student_id']
            even_info['holyevent_type'] = self.evenType
            db.add_even(even_info)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HolyEventBaptismInterFace(None)
    window.show()
    sys.exit(app.exec())
