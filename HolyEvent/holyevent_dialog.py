import enum
import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QLabel, QAbstractItemView, QHeaderView, \
    QCheckBox, QTableWidgetItem, QDialog
from qfluentwidgets import LineEdit, InfoBar, PushButton, TableWidget, \
    SearchLineEdit, ComboBox, CalendarPicker, setCustomStyleSheet

from DataBase.family_db import FamilyDB
from DataBase.holyevent_db import HolyEventDB
from DataBase.student_db import StudentDB
from student.stduent_basetemp import QUERY_TYPE
from utils.custom_style import ADD_BUTTON_STYLE, DELETE_BUTTON_STYLE, MODIFY_BUTTON_STYLE, UPDATE_BUTTON_STYLE
from utils.utils_tool import qdate_to_timestamp, timestamp_to_date, get_datestr_from_timestamp


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

        #----------------------人物1 姓名圣名 ------------------------------#
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
        # ----------------------人物1 end ---------------------------------#
        #-----------------------人物2 姓名圣名 ------------------------------#

        self.horizontalLayout_person2 = QHBoxLayout()
        self.label_9 = QLabel()

        self.horizontalLayout_person2.addWidget(self.label_9)

        self.lineEdit_9 = LineEdit()

        self.horizontalLayout_person2.addWidget(self.lineEdit_9)

        self.label_10 = QLabel()

        self.horizontalLayout_person2.addWidget(self.label_10)

        self.lineEdit_10 = LineEdit()

        self.horizontalLayout_person2.addWidget(self.lineEdit_10)

        self.verticalLayout_2.addLayout(self.horizontalLayout_person2)
        # ----------------------人物2 end ---------------------------------#
        self.horizontalLayout_2 = QHBoxLayout()
        self.label_4 = QLabel()

        self.horizontalLayout_2.addWidget(self.label_4)

        self.genderCombo = ComboBox(self)  # 创建一个下拉框组件用于选择性别
        self.genderCombo.addItem("男", userData=0)
        self.genderCombo.addItem("女", userData=1)
        self.genderCombo.setMinimumWidth(100)

        self.horizontalLayout_2.addWidget(self.genderCombo)

        self.label_5 = QLabel()

        self.horizontalLayout_2.addWidget(self.label_5)

        self.calendarPicker = CalendarPicker()

        self.horizontalLayout_2.addWidget(self.calendarPicker)

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

        # self.horizontalLayout_5 = QHBoxLayout()
        # self.pushButton_1 = PushButton()
        #
        # self.horizontalLayout_5.addWidget(self.pushButton_1)
        #
        # self.pushButton_2 = PushButton()
        #
        # self.horizontalLayout_5.addWidget(self.pushButton_2)
        #
        # self.pushButton_3 = PushButton()
        #
        # self.horizontalLayout_5.addWidget(self.pushButton_3)
        #
        # self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.main_verticalLayout.addLayout(self.horizontalLayout_7)

        self.verticalLayout = QVBoxLayout()

        self.horizontalLayout_6 = QHBoxLayout()

        self.pushButton_1 = PushButton()
        setCustomStyleSheet(self.pushButton_1, ADD_BUTTON_STYLE, ADD_BUTTON_STYLE)

        self.horizontalLayout_6.addWidget(self.pushButton_1)

        self.pushButton_2 = PushButton()
        setCustomStyleSheet(self.pushButton_2, DELETE_BUTTON_STYLE, DELETE_BUTTON_STYLE)

        self.horizontalLayout_6.addWidget(self.pushButton_2)

        self.searchInput = SearchLineEdit(self)
        self.searchInput.setPlaceholderText('Search')
        self.searchInput.setFixedWidth(500)

        self.horizontalLayout_6.addWidget(self.searchInput)

        self.pushButton_3 = PushButton()
        setCustomStyleSheet(self.pushButton_3, MODIFY_BUTTON_STYLE, MODIFY_BUTTON_STYLE)

        self.horizontalLayout_6.addWidget(self.pushButton_3)

        self.pushButton_4 = PushButton()
        setCustomStyleSheet(self.pushButton_4, UPDATE_BUTTON_STYLE, UPDATE_BUTTON_STYLE)

        self.horizontalLayout_6.addWidget(self.pushButton_4)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.tableWidget = TableWidget()
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.verticalLayout.addWidget(self.tableWidget)

        self.main_verticalLayout.addLayout(self.verticalLayout)

        # self.lineEdit_1.setMaximumWidth(200)
        # self.lineEdit_2.setMaximumWidth(200)
        # self.lineEdit_4.setMaximumWidth(200)
        # self.lineEdit_5.setMaximumWidth(200)
        # self.lineEdit_6.setMaximumWidth(200)
        # self.lineEdit_7.setMaximumWidth(600)
        # self.label_2.setMaximumWidth(50)
        # self.label_3.setMaximumWidth(50)
        # self.label_4.setMaximumWidth(50)
        # self.label_5.setMaximumWidth(50)
        # self.label_6.setMaximumWidth(50)
        # self.label_7.setMaximumWidth(50)
        # self.label_8.setMaximumWidth(50)

    @staticmethod
    def set_viewWidget_data(tableWidget, header_info, datas):
        tableWidget.clearContents()
        tableWidget.setRowCount(len(datas))
        for row, data in enumerate(datas):
            checkBox = QCheckBox()
            tableWidget.setCellWidget(row, 0, checkBox)
            for column, key in enumerate(header_info):
                if key == "holyevent_date":
                    value = data.get(key, "")
                    item = QTableWidgetItem(str(get_datestr_from_timestamp(value)))
                else:
                    value = data.get(key, "")
                    item = QTableWidgetItem(str(value))
                tableWidget.setItem(row, column + 1, item)

# 圣洗圣事
class HolyEventBaptismInterFace(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.update_even_info_flag = False
        self.even_info = None
        self.verticalLayout = None
        self.role = parent.role
        self.school_info = parent.school_info
        self.data_from_SQL = False
        self.person_info = {}
        self.temp_family_id = 1
        self.evenType = 0
        # self.setObjectName("BaseHolyEventInterFace")
        self.baseStudentFuncTemp = BaseEvenFuncTemp()
        self.baseStudentFuncTemp.label_9.hide()
        self.baseStudentFuncTemp.label_10.hide()
        self.baseStudentFuncTemp.lineEdit_9.hide()
        self.baseStudentFuncTemp.lineEdit_10.hide()
        self.even_viewTable_header_info = [
            "", "姓名", "圣名", "施行人", "见证人", "堂区", "日期", "备注"
        ]
        self.even_database_header_info = [
            'holyevent_p1_name', 'holyevent_p1_holyname', 'holyevent_implementer',
            'holyevent_witness', 'holyevent_school_id', 'holyevent_date', 'holyevent_note'
        ]

        self.setup_ui()
        self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
        self.set_default_data()

    def set_default_data(self):
        with FamilyDB() as family_db:
            temp_family = family_db.fetch_tempfamily_with_school_id("临时", self.school_info["school_id"])
            self.temp_family_id = temp_family["family_id"]
            if self.temp_family_id is None:
                self.temp_family_id = 1


    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp.main_verticalLayout)

        ##
        self.baseStudentFuncTemp.label_2.setText("姓名")
        self.baseStudentFuncTemp.label_3.setText("圣名")
        self.baseStudentFuncTemp.label_4.setText("性别")
        self.baseStudentFuncTemp.label_5.setText("日期")
        self.baseStudentFuncTemp.label_6.setText("施行人")
        self.baseStudentFuncTemp.label_7.setText("见证人")
        self.baseStudentFuncTemp.label_8.setText("备注")
        self.baseStudentFuncTemp.pushButton_1.setText("添加")
        self.baseStudentFuncTemp.pushButton_2.setText("删除")
        self.baseStudentFuncTemp.pushButton_3.setText("修改选中的事件")
        self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")

        self.baseStudentFuncTemp.tableWidget.setColumnCount(len(self.even_viewTable_header_info))
        self.baseStudentFuncTemp.tableWidget.setHorizontalHeaderLabels(self.even_viewTable_header_info)
        self.baseStudentFuncTemp.searchInput.searchSignal.connect(self.query_even_info_with_like)
        self.baseStudentFuncTemp.searchInput.returnPressed.connect(self.query_even_info_with_like)

        self.baseStudentFuncTemp.pushButton_1.clicked.connect(self.add_even_info)
        self.baseStudentFuncTemp.pushButton_2.clicked.connect(self.delete_even_info)
        self.baseStudentFuncTemp.pushButton_3.clicked.connect(self.update_even_info)

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

        if not self.baseStudentFuncTemp.lineEdit_5.text().strip():
            errors.append("请输入施行人")  # 验证学号是否填写，如果未填写，添加错误信息

        if self.baseStudentFuncTemp.calendarPicker.date.year() == 0:
            errors.append("请选择日期")  # 验证学号是否填写，如果未填写，添加错误信息


        return errors  # 返回所有错误信息

    def _geteveninfo(self):
        even_info = {
            'holyevent_p1_id': '',
            'holyevent_p1_name': self.baseStudentFuncTemp.lineEdit_1.text(),
            'holyevent_p1_holyname': self.baseStudentFuncTemp.lineEdit_2.text(),
            'holyevent_p1_gender': self.baseStudentFuncTemp.genderCombo.currentData(),
            'holyevent_p2_id': '',
            'holyevent_p2_name': '',
            'holyevent_p2_holyname': '',
            'holyevent_implementer': self.baseStudentFuncTemp.lineEdit_5.text(),
            'holyevent_witness': self.baseStudentFuncTemp.lineEdit_6.text(),
            'holyevent_school_id': "",
            'holyevent_date': qdate_to_timestamp(self.baseStudentFuncTemp.calendarPicker.date),
            'holyevent_note': self.baseStudentFuncTemp.lineEdit_7.text()
        }
        return even_info

    def seteveninfoFromParent(self, person_info):
        self.person_info = person_info
        self.data_from_SQL = True
        self.baseStudentFuncTemp.lineEdit_1.setText(person_info['student_name'])
        self.baseStudentFuncTemp.lineEdit_2.setText(person_info['student_holyname'])
        print(person_info['student_gender'])
        self.baseStudentFuncTemp.genderCombo.setCurrentIndex(person_info['student_gender'])

    def seteveninfoFromSelf(self, even_info):
        self.baseStudentFuncTemp.lineEdit_1.setText(even_info['holyevent_p1_name'])
        self.baseStudentFuncTemp.lineEdit_2.setText(even_info['holyevent_p1_holyname'])
        self.baseStudentFuncTemp.genderCombo.setCurrentIndex(even_info['holyevent_p1_gender'])
        self.baseStudentFuncTemp.lineEdit_5.setText(even_info['holyevent_implementer'])
        self.baseStudentFuncTemp.lineEdit_6.setText(even_info['holyevent_witness'])
        self.baseStudentFuncTemp.lineEdit_7.setText(even_info['holyevent_note'])
        self.baseStudentFuncTemp.calendarPicker.setDate(timestamp_to_date(even_info['holyevent_date']))

    def add_even_info(self):
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        even_info = self._geteveninfo()
        if self.data_from_SQL:
            # 如果是从数据库中找到的人员，就修改圣名即可
            with StudentDB() as db:
                db.update_student_holyname(self.person_info['student_id'], even_info['holyevent_p1_holyname'])
                self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
        else:
            # 如果是新建的人，就添加人物数据并添加到零时家庭中
            with StudentDB() as db:
                even_info = self._geteveninfo()
                StudentInfo = {
                    "student_name": even_info['holyevent_p1_name'],
                    "student_gender": even_info['holyevent_p1_gender'],
                    "student_phonenum": "",  # 性别字段与对应的下拉框
                    "student_holyname": even_info['holyevent_p1_holyname'],  # 班级字段与对应的下拉框
                    "student_family_id": self.temp_family_id,  # 语文字段与对应的输入框
                    "student_school_id": self.school_info["school_id"]  # 语文字段与对应的输入框
                }
                self.person_info['student_id'] = db.add_student(StudentInfo)
        with HolyEventDB() as db:
            even_info['holyevent_p1_id'] = self.person_info['student_id']
            even_info['holyevent_type'] = self.evenType
            db.add_even(even_info)
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)

    def delete_even_info(self):
        idx = self.baseStudentFuncTemp.tableWidget.currentRow()
        if idx == -1:
            return
        with HolyEventDB() as db:
            db.delete_event(self.even_info[idx]["holyevent_id"])
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)

    def update_even_info(self):
        if self.update_even_info_flag:
            idx = self.baseStudentFuncTemp.tableWidget.currentRow()
            self.update_even_info_flag = False
            even_info = self._geteveninfo()
            with StudentDB() as db:
                db.update_student_holyname(self.even_info[idx]['holyevent_p1_id'], even_info['holyevent_p1_holyname'])
            with HolyEventDB() as db:
                even_info['holyevent_p1_id'] = self.even_info[idx]['holyevent_p1_id']
                even_info['holyevent_type'] = self.evenType
                db.update_even(even_info)
                self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
            self.baseStudentFuncTemp.pushButton_3.setText("修改选中的事件")
            self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")
        else:
            idx = self.baseStudentFuncTemp.tableWidget.currentRow()
            if idx == -1:
                InfoBar.error(title="先选择事件", parent=self,
                              duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
                return
            print(self.even_info)
            print(idx)
            self.seteveninfoFromSelf(self.even_info[idx])
            self.update_even_info_flag = True
            self.baseStudentFuncTemp.pushButton_3.setText("点击确认保存修改")
            self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")

# 坚振圣事
class HolyEventConfirmationInterFace(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.update_even_info_flag = False
        self.even_info = None
        self.verticalLayout = None
        self.role = parent.role
        self.school_info = parent.school_info
        self.data_from_SQL = False
        self.person_info = {}
        self.temp_family_id = 1
        self.evenType = 1
        # self.setObjectName("BaseHolyEventInterFace")
        self.baseStudentFuncTemp = BaseEvenFuncTemp()
        self.baseStudentFuncTemp.label_9.hide()
        self.baseStudentFuncTemp.label_10.hide()
        self.baseStudentFuncTemp.lineEdit_9.hide()
        self.baseStudentFuncTemp.lineEdit_10.hide()
        self.even_viewTable_header_info = [
            "", "姓名", "圣名", "施行人", "见证人", "堂区", "日期", "备注"
        ]
        self.even_database_header_info = [
            'holyevent_p1_name', 'holyevent_p1_holyname', 'holyevent_implementer',
            'holyevent_witness', 'holyevent_school_id', 'holyevent_date', 'holyevent_note'
        ]

        self.setup_ui()
        self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
        self.set_default_data()

    def set_default_data(self):
        with FamilyDB() as family_db:
            temp_family = family_db.fetch_tempfamily_with_school_id("临时", self.school_info["school_id"])
            self.temp_family_id = temp_family["family_id"]
            if self.temp_family_id is None:
                self.temp_family_id = 1


    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp.main_verticalLayout)

        ##
        self.baseStudentFuncTemp.label_2.setText("姓名")
        self.baseStudentFuncTemp.label_3.setText("圣名")
        self.baseStudentFuncTemp.label_4.setText("性别")
        self.baseStudentFuncTemp.label_5.setText("日期")
        self.baseStudentFuncTemp.label_6.setText("施行人")
        self.baseStudentFuncTemp.label_7.setText("见证人")
        self.baseStudentFuncTemp.label_8.setText("备注")
        self.baseStudentFuncTemp.pushButton_1.setText("添加")
        self.baseStudentFuncTemp.pushButton_2.setText("删除")
        self.baseStudentFuncTemp.pushButton_3.setText("修改选中的事件")
        self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")

        self.baseStudentFuncTemp.tableWidget.setColumnCount(len(self.even_viewTable_header_info))
        self.baseStudentFuncTemp.tableWidget.setHorizontalHeaderLabels(self.even_viewTable_header_info)
        self.baseStudentFuncTemp.searchInput.searchSignal.connect(self.query_even_info_with_like)
        self.baseStudentFuncTemp.searchInput.returnPressed.connect(self.query_even_info_with_like)

        self.baseStudentFuncTemp.pushButton_1.clicked.connect(self.add_even_info)
        self.baseStudentFuncTemp.pushButton_2.clicked.connect(self.delete_even_info)
        self.baseStudentFuncTemp.pushButton_3.clicked.connect(self.update_even_info)

        self.baseStudentFuncTemp.label_1.setPixmap(QPixmap("./resource/pic/c2.png"))

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

        if not self.baseStudentFuncTemp.lineEdit_5.text().strip():
            errors.append("请输入施行人")  # 验证学号是否填写，如果未填写，添加错误信息

        if self.baseStudentFuncTemp.calendarPicker.date.year() == 0:
            errors.append("请选择日期")  # 验证学号是否填写，如果未填写，添加错误信息

        return errors  # 返回所有错误信息

    def _geteveninfo(self):
        even_info = {
            'holyevent_p1_id': '',
            'holyevent_p1_name': self.baseStudentFuncTemp.lineEdit_1.text(),
            'holyevent_p1_holyname': self.baseStudentFuncTemp.lineEdit_2.text(),
            'holyevent_p1_gender': self.baseStudentFuncTemp.genderCombo.currentData(),
            'holyevent_p2_id': '',
            'holyevent_p2_name': '',
            'holyevent_p2_holyname': '',
            'holyevent_implementer': self.baseStudentFuncTemp.lineEdit_5.text(),
            'holyevent_witness': self.baseStudentFuncTemp.lineEdit_6.text(),
            'holyevent_school_id': "",
            'holyevent_date': qdate_to_timestamp(self.baseStudentFuncTemp.calendarPicker.date),
            'holyevent_note': self.baseStudentFuncTemp.lineEdit_7.text()
        }
        return even_info

    def seteveninfoFromParent(self, person_info):
        self.person_info = person_info
        self.data_from_SQL = True
        self.baseStudentFuncTemp.lineEdit_1.setText(person_info['student_name'])
        self.baseStudentFuncTemp.lineEdit_2.setText(person_info['student_holyname'])
        print(person_info['student_gender'])
        self.baseStudentFuncTemp.genderCombo.setCurrentIndex(person_info['student_gender'])

    def seteveninfoFromSelf(self, even_info):
        self.baseStudentFuncTemp.lineEdit_1.setText(even_info['holyevent_p1_name'])
        self.baseStudentFuncTemp.lineEdit_2.setText(even_info['holyevent_p1_holyname'])
        self.baseStudentFuncTemp.genderCombo.setCurrentIndex(even_info['holyevent_p1_gender'])
        self.baseStudentFuncTemp.lineEdit_5.setText(even_info['holyevent_implementer'])
        self.baseStudentFuncTemp.lineEdit_6.setText(even_info['holyevent_witness'])
        self.baseStudentFuncTemp.lineEdit_7.setText(even_info['holyevent_note'])
        self.baseStudentFuncTemp.calendarPicker.setDate(timestamp_to_date(even_info['holyevent_date']))

    def add_even_info(self):
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        even_info = self._geteveninfo()
        if self.data_from_SQL:
            # 如果是从数据库中找到的人员，就修改圣名即可
            pass
        else:
            # 如果是新建的人，就添加人物数据并添加到零时家庭中
            with StudentDB() as db:
                even_info = self._geteveninfo()
                StudentInfo = {
                    "student_name": even_info['holyevent_p1_name'],
                    "student_gender": even_info['holyevent_p1_gender'],
                    "student_phonenum": "",  # 性别字段与对应的下拉框
                    "student_holyname": even_info['holyevent_p1_holyname'],  # 班级字段与对应的下拉框
                    "student_family_id": self.temp_family_id,  # 语文字段与对应的输入框
                    "student_school_id": self.school_info["school_id"]  # 语文字段与对应的输入框
                }
                self.person_info['student_id'] = db.add_student(StudentInfo)
        with HolyEventDB() as db:
            even_info['holyevent_p1_id'] = self.person_info['student_id']
            even_info['holyevent_type'] = self.evenType
            print(even_info)
            db.add_even(even_info)
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)

    def delete_even_info(self):
        idx = self.baseStudentFuncTemp.tableWidget.currentRow()
        if idx == -1:
            return
        with HolyEventDB() as db:
            db.delete_event(self.even_info[idx]["holyevent_id"])
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)

    def update_even_info(self):
        if self.update_even_info_flag:
            idx = self.baseStudentFuncTemp.tableWidget.currentRow()
            self.update_even_info_flag = False
            even_info = self._geteveninfo()
            with StudentDB() as db:
                db.update_student_holyname(self.even_info[idx]['holyevent_p1_id'], even_info['holyevent_p1_holyname'])
            with HolyEventDB() as db:
                even_info['holyevent_p1_id'] = self.even_info[idx]['holyevent_p1_id']
                even_info['holyevent_type'] = self.evenType
                db.update_even(even_info)
                self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
            self.baseStudentFuncTemp.pushButton_3.setText("修改选中的事件")
            self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")
        else:
            idx = self.baseStudentFuncTemp.tableWidget.currentRow()
            if idx == -1:
                InfoBar.error(title="先选择事件", parent=self,
                              duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
                return
            print(self.even_info)
            print(idx)
            self.seteveninfoFromSelf(self.even_info[idx])
            self.update_even_info_flag = True
            self.baseStudentFuncTemp.pushButton_3.setText("点击确认保存修改")
            self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")

# 婚姻圣事
class HolyEventmarriageInterFace(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.update_even_info_flag = False
        self.even_info = None
        self.verticalLayout = None
        self.role = parent.role
        self.school_info = parent.school_info
        self.data_from_SQL = False
        self.person_info = {}
        self.temp_family_id = 1
        self.evenType = 1
        # self.setObjectName("BaseHolyEventInterFace")
        self.baseStudentFuncTemp = BaseEvenFuncTemp()
        self.baseStudentFuncTemp.genderCombo.hide()
        self.baseStudentFuncTemp.label_4.hide()
        self.even_viewTable_header_info = [
            "", "姓名", "圣名", "施行人", "见证人", "堂区", "日期", "备注"
        ]
        self.even_database_header_info = [
            'holyevent_p1_name', 'holyevent_p1_holyname', 'holyevent_implementer',
            'holyevent_witness', 'holyevent_school_id', 'holyevent_date', 'holyevent_note'
        ]

        self.setup_ui()
        self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
        self.set_default_data()

    def set_default_data(self):
        with FamilyDB() as family_db:
            temp_family = family_db.fetch_tempfamily_with_school_id("临时", self.school_info["school_id"])
            self.temp_family_id = temp_family["family_id"]
            if self.temp_family_id is None:
                self.temp_family_id = 1


    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp.main_verticalLayout)

        ##
        self.baseStudentFuncTemp.label_2.setText("男方姓名")
        self.baseStudentFuncTemp.label_3.setText("男方圣名")
        self.baseStudentFuncTemp.label_4.setText("性别")
        self.baseStudentFuncTemp.label_5.setText("日期")
        self.baseStudentFuncTemp.label_6.setText("施行人")
        self.baseStudentFuncTemp.label_7.setText("见证人")
        self.baseStudentFuncTemp.label_8.setText("备注")
        self.baseStudentFuncTemp.label_9.setText("女方姓名")
        self.baseStudentFuncTemp.label_10.setText("女方圣名")
        self.baseStudentFuncTemp.pushButton_1.setText("添加")
        self.baseStudentFuncTemp.pushButton_2.setText("删除")
        self.baseStudentFuncTemp.pushButton_3.setText("修改选中的事件")
        self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")

        self.baseStudentFuncTemp.tableWidget.setColumnCount(len(self.even_viewTable_header_info))
        self.baseStudentFuncTemp.tableWidget.setHorizontalHeaderLabels(self.even_viewTable_header_info)
        self.baseStudentFuncTemp.searchInput.searchSignal.connect(self.query_even_info_with_like)
        self.baseStudentFuncTemp.searchInput.returnPressed.connect(self.query_even_info_with_like)

        self.baseStudentFuncTemp.pushButton_1.clicked.connect(self.add_even_info)
        self.baseStudentFuncTemp.pushButton_2.clicked.connect(self.delete_even_info)
        self.baseStudentFuncTemp.pushButton_3.clicked.connect(self.update_even_info)

        self.baseStudentFuncTemp.label_1.setPixmap(QPixmap("./resource/pic/c3.png"))

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

        if not self.baseStudentFuncTemp.lineEdit_5.text().strip():
            errors.append("请输入施行人")  # 验证学号是否填写，如果未填写，添加错误信息

        if self.baseStudentFuncTemp.calendarPicker.date.year() == 0:
            errors.append("请选择日期")  # 验证学号是否填写，如果未填写，添加错误信息

        return errors  # 返回所有错误信息

    def _geteveninfo(self):
        even_info = {
            'holyevent_p1_id': '',
            'holyevent_p1_name': self.baseStudentFuncTemp.lineEdit_1.text(),
            'holyevent_p1_holyname': self.baseStudentFuncTemp.lineEdit_2.text(),
            'holyevent_p1_gender': self.baseStudentFuncTemp.genderCombo.currentData(),
            'holyevent_p2_id': '',
            'holyevent_p2_name': '',
            'holyevent_p2_holyname': '',
            'holyevent_implementer': self.baseStudentFuncTemp.lineEdit_5.text(),
            'holyevent_witness': self.baseStudentFuncTemp.lineEdit_6.text(),
            'holyevent_school_id': "",
            'holyevent_date': qdate_to_timestamp(self.baseStudentFuncTemp.calendarPicker.date),
            'holyevent_note': self.baseStudentFuncTemp.lineEdit_7.text()
        }
        return even_info

    def seteveninfoFromParent(self, person_info):
        self.person_info = person_info
        self.data_from_SQL = True
        self.baseStudentFuncTemp.lineEdit_1.setText(person_info['student_name'])
        self.baseStudentFuncTemp.lineEdit_2.setText(person_info['student_holyname'])
        print(person_info['student_gender'])
        self.baseStudentFuncTemp.genderCombo.setCurrentIndex(person_info['student_gender'])

    def seteveninfoFromSelf(self, even_info):
        self.baseStudentFuncTemp.lineEdit_1.setText(even_info['holyevent_p1_name'])
        self.baseStudentFuncTemp.lineEdit_2.setText(even_info['holyevent_p1_holyname'])
        self.baseStudentFuncTemp.genderCombo.setCurrentIndex(even_info['holyevent_p1_gender'])
        self.baseStudentFuncTemp.lineEdit_5.setText(even_info['holyevent_implementer'])
        self.baseStudentFuncTemp.lineEdit_6.setText(even_info['holyevent_witness'])
        self.baseStudentFuncTemp.lineEdit_7.setText(even_info['holyevent_note'])
        self.baseStudentFuncTemp.calendarPicker.setDate(timestamp_to_date(even_info['holyevent_date']))

    def add_even_info(self):
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        even_info = self._geteveninfo()
        if self.data_from_SQL:
            # 如果是从数据库中找到的人员，就修改圣名即可
            pass
        else:
            # 如果是新建的人，就添加人物数据并添加到零时家庭中
            with StudentDB() as db:
                even_info = self._geteveninfo()
                StudentInfo = {
                    "student_name": even_info['holyevent_p1_name'],
                    "student_gender": even_info['holyevent_p1_gender'],
                    "student_phonenum": "",  # 性别字段与对应的下拉框
                    "student_holyname": even_info['holyevent_p1_holyname'],  # 班级字段与对应的下拉框
                    "student_family_id": self.temp_family_id,  # 语文字段与对应的输入框
                    "student_school_id": self.school_info["school_id"]  # 语文字段与对应的输入框
                }
                self.person_info['student_id'] = db.add_student(StudentInfo)
        with HolyEventDB() as db:
            even_info['holyevent_p1_id'] = self.person_info['student_id']
            even_info['holyevent_type'] = self.evenType
            print(even_info)
            db.add_even(even_info)
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)

    def delete_even_info(self):
        idx = self.baseStudentFuncTemp.tableWidget.currentRow()
        if idx == -1:
            return
        with HolyEventDB() as db:
            db.delete_event(self.even_info[idx]["holyevent_id"])
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)

    def update_even_info(self):
        if self.update_even_info_flag:
            idx = self.baseStudentFuncTemp.tableWidget.currentRow()
            self.update_even_info_flag = False
            even_info = self._geteveninfo()
            with StudentDB() as db:
                db.update_student_holyname(self.even_info[idx]['holyevent_p1_id'], even_info['holyevent_p1_holyname'])
            with HolyEventDB() as db:
                even_info['holyevent_p1_id'] = self.even_info[idx]['holyevent_p1_id']
                even_info['holyevent_type'] = self.evenType
                db.update_even(even_info)
                self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
            self.baseStudentFuncTemp.pushButton_3.setText("修改选中的事件")
            self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")
        else:
            idx = self.baseStudentFuncTemp.tableWidget.currentRow()
            if idx == -1:
                InfoBar.error(title="先选择事件", parent=self,
                              duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
                return
            print(self.even_info)
            print(idx)
            self.seteveninfoFromSelf(self.even_info[idx])
            self.update_even_info_flag = True
            self.baseStudentFuncTemp.pushButton_3.setText("点击确认保存修改")
            self.baseStudentFuncTemp.pushButton_4.setText("放弃修改")

class testclass():
    def __init__(self):
        self.role = 1
        self.school_info = {
            "school_id": 1,
            "school_name": "崇义小学",
            "school_address": "崇义小学地址",
            "school_phone": "1234567890",
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    testclass = testclass()
    window = HolyEventmarriageInterFace(testclass)
    window.show()
    sys.exit(app.exec())
