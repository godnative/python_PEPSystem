import enum
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QApplication, QGridLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, StrongBodyLabel, InfoBar

from DataBase.holyevent_db import HolyEventDB
from student.stduent_basetemp import BaseStudentFuncTemp, QUERY_TYPE, Student_Widget


class HOLY_EVENT_TYPE(enum.Enum):
    HOLY_EVENT_BAPTISM = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class BaseEvenDialog(MessageBoxBase):  # 定义一个学生信息弹窗的基类，继承自 MessageBoxBase
    def __init__(self, title, student_info, parent=None):  # 初始化方法，接收弹窗标题和父窗口作为参数
        super().__init__(parent)  # 调用父类的初始化方法，设置父窗口
        self.title = title  # 保存弹窗标题，用于区分弹窗用途（如添加或修改学生信息）
        self.cur_school_id = 1
        self.student_info = student_info
        self.setup_ui()  # 调用界面设置方法，初始化弹窗界面

    def setup_ui(self):  # 定义设置用户界面的方法
        self.titleLabel = SubtitleLabel(self.title, self)  # 创建一个 SubtitleLabel 实例，传入标题文本和父窗口
        self.viewLayout.addWidget(self.titleLabel)  # 将标题控件添加到布局中
        self.viewLayout.setAlignment(self.titleLabel, Qt.AlignmentFlag.AlignCenter)  # 设置标题控件在布局中的对齐方式为居中

        self.grid_layout = QGridLayout()  # 创建一个栅格布局对象，用于对控件进行行列排布
        self.viewLayout.addLayout(self.grid_layout)  # 将栅格布局添加到主视图布局中

        # 创建输入控件
        self.holyevent_p1_name = LineEdit(self)  # 创建一个单行文本输入框用于输入姓名
        self.holynameInput = LineEdit(self)  # 创建一个单行文本输入框用于输入姓名
        self.holyevent_witness = LineEdit(self)
        self.holyevent_implementer = LineEdit(self)
        self.holyevent_note = LineEdit(self)
        self.holyevent_date = LineEdit(self)

        # 定义字段标签与控件的映射
        fields = [
            ("姓名：", self.holyevent_p1_name),  # 姓名字段与对应的输入框
            ("圣名：", self.holynameInput),  # 性别字段与对应的下拉框
            ("见证人：", self.holyevent_witness),  # 语文字段与对应的输入框
            ("施行人：", self.holyevent_implementer),  # 数学字段与对应的输入框
            ("备注：", self.holyevent_note),  # 班级字段与对应的下拉框
            ("日期：", self.holyevent_date)  # 班级字段与对应的下拉框
        ]

        # 遍历字段，添加到栅格布局中
        for row, (label_text, widget) in enumerate(fields):  # 使用 enumerate 获取字段的行号
            label = StrongBodyLabel(label_text, self)  # 创建加粗的标签
            self.grid_layout.addWidget(label, row, 0)  # 将标签添加到栅格布局的第一列
            self.grid_layout.addWidget(widget, row, 1)  # 将控件添加到栅格布局的第二列

        # 设置列拉伸
        self.grid_layout.setColumnStretch(1, 1)  # 设置第二列的列拉伸系数为 1，确保控件能够自动适应窗口大小

        # 设置标签对齐方式
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 将控件对齐到左侧

        # 修改按钮文本
        self.yesButton.setText('确定')  # 将确认按钮文本设置为“确定”
        self.cancelButton.setText('取消')  # 将取消按钮文本设置为“取消”

        # 设置输入框的宽度
        for widget in [self.holyevent_p1_name, self.holynameInput, self.holyevent_witness,
                       self.holyevent_implementer, self.holyevent_note, self.holyevent_date]:
            widget.setMinimumWidth(200)  # 为每个输入框设置最小宽度为 200

        # 将焦点定位到姓名输入框
        self.holyevent_p1_name.setFocus()  # 设置焦点到姓名输入框，使其在弹出时默认获取焦点

        # 确保“确定”按钮不会自动对焦
        self.yesButton.setDefault(False)  # 取消“确定”按钮的默认焦点
        self.yesButton.setAutoDefault(False)  # 禁止“确定”按钮自动成为默认按钮

        self.holyevent_p1_name.setText(self.student_info["student_name"])

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.holyevent_p1_name.text().strip():
            errors.append("请输入姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.holynameInput.text().strip():
            errors.append("请输入学号")  # 验证学号是否填写，如果未填写，添加错误信息

        if not self.holyevent_witness.text().strip():
            errors.append("请输入姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.holyevent_implementer.text().strip():
            errors.append("请输入学号")  # 验证学号是否填写，如果未填写，添加错误信息

        return errors  # 返回所有错误信息

    def accept(self):
        # 对数据进行验证
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        # 如果验证通过，调用父类的 accept 方法，接收数据并关闭对话框
        super().accept()

    def get_InputEvenDialoginfo(self):
        EvenInfo = {
            "holyevent_p1_name": self.holyevent_p1_name.text(),
            "holynameInput": self.holynameInput.text(),
            "holyevent_witness": self.holyevent_witness.text(),  # 性别字段与对应的下拉框
            "holyevent_implementer": self.holyevent_implementer.text(),  # 班级字段与对应的下拉框
            "holyevent_note": self.holyevent_note.text(),  # 语文字段与对应的输入框
            "holyevent_date": self.holyevent_date.text()  # 语文字段与对应的输入框
        }
        return EvenInfo


class AddEventDialog(BaseEvenDialog):  # 定义一个用于添加学生的弹窗类，继承自 BaseStudentDialog
    def __init__(self, student_info, parent=None):  # 初始化方法，接收父窗口作为参数，默认为 None
        super().__init__('添加圣洗圣事', student_info, parent)  # 调用父类的初始化方法，设置弹窗标题为“添加学生”，并传递父窗口
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能


class HolyEventBaptismInterFace(QWidget):
    def __init__(self, curSchool):
        super().__init__()
        self.even_info = None
        self.verticalLayout = None
        self.curSchool = curSchool
        self.evenType = HOLY_EVENT_TYPE.HOLY_EVENT_BAPTISM
        # self.setObjectName("BaseHolyEventInterFace")
        self.baseStudentFuncTemp_1 = BaseStudentFuncTemp()
        self.student_widget = Student_Widget(self.curSchool)
        self.even_viewTable_header_info = [
            "", "人员", "圣名", "日期", "施行人", "见证人", "堂区", "备注"
        ]
        self.even_database_header_info = [
            'holyevent_p1_name', 'holyevent_p1_name', 'holyevent_date', 'holyevent_implementer',
            'holyevent_witness', 'holyevent_school_id', 'holyevent_note'
        ]

        self.setup_ui()
        self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)

    def setup_ui(self):
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_1.main_verticalLayout)
        self.verticalLayout.addWidget(self.student_widget)

        self.baseStudentFuncTemp_1.tableWidget.setColumnCount(len(self.even_viewTable_header_info))
        self.baseStudentFuncTemp_1.tableWidget.setHorizontalHeaderLabels(self.even_viewTable_header_info)
        self.baseStudentFuncTemp_1.searchInput.searchSignal.connect(self.query_even_info_with_like)
        self.baseStudentFuncTemp_1.searchInput.returnPressed.connect(self.query_even_info_with_like)
        self.student_widget.baseStudentFuncTemp_1.button_1.hide()
        self.student_widget.baseStudentFuncTemp_1.button_2.setText("从选中人员新建事件")
        self.student_widget.baseStudentFuncTemp_1.button_2.clicked.connect(self.add_even_info_with_persion)
        self.student_widget.baseStudentFuncTemp_1.button_3.hide()

        self.baseStudentFuncTemp_1.button_1.clicked.connect(self.add_even_info)

    def add_even_info_with_persion(self):
        if self.student_widget.baseStudentFuncTemp_1.tableWidget.currentRow() == -1:
            print("没有选择")
        else:
            student_info = self.student_widget.students[
                self.student_widget.baseStudentFuncTemp_1.tableWidget.currentRow()]
            w = AddEventDialog(student_info, self)
            if w.exec():
                print(w.get_InputEvenDialoginfo())

    def query_even_info_with_like(self):
        if self.baseStudentFuncTemp_1.searchInput.text() == "":
            self.load_even_data(QUERY_TYPE.QUERY_ALL, self.evenType, None)
        else:
            self.load_even_data(QUERY_TYPE.QUERY_LIKE, self.evenType, self.baseStudentFuncTemp_1.searchInput.text())

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

        self.baseStudentFuncTemp_1.set_viewWidget_data(self.baseStudentFuncTemp_1.tableWidget,
                                                       self.even_database_header_info, self.even_info)

    def add_even_info(self):
        w = AddEventDialog(None, self)
        if w.exec():
            print(w.get_InputEvenDialoginfo())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StudentInterface()
    window.show()
    sys.exit(app.exec())
