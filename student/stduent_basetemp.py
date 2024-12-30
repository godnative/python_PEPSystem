# student/student_dialog.py文件中
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, \
    QHeaderView, QApplication, QAbstractItemView, QGridLayout  # 导入 PyQt6 模块中的 QGridLayout，用于栅格布局
from qfluentwidgets import TableWidget, PushButton, CardWidget, setCustomStyleSheet, \
    SearchLineEdit, LineEdit, ComboBox, StrongBodyLabel  # 导入 qfluentwidgets 模块中的组件

from utils.custom_style import ADD_BUTTON_STYLE, BATCH_DELETE_BUTTON_STYLE


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

        self.button_layout.addWidget(self.button_1)
        self.button_layout.addWidget(self.searchInput)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.button_2)

        self.main_verticalLayout.addWidget(card_widget)

        self.tableWidget = TableWidget(self)
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.main_verticalLayout.addWidget(self.tableWidget)
        self.setStyleSheet('StudentInterface{background-color:white}')


class BaseStudentInfoTemp(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.grid_layout = QGridLayout()  # 创建一个栅格布局对象，用于对控件进行行列排布

        # 创建输入控件
        self.nameInput = LineEdit(self)  # 创建一个单行文本输入框用于输入姓名
        self.genderCombo = ComboBox(self)  # 创建一个下拉框组件用于选择性别
        self.genderCombo.addItems(['男', '女'])  # 为下拉框添加两个选项：男和女
        self.familyCombo = ComboBox(self)  # 创建一个下拉框组件用于选择班级
        self.phoneInput = LineEdit(self)  # 创建一个单行文本输入框用于输入语文成绩
        self.holyNameInput = LineEdit(self)  # 创建一个单行文本输入框用于输入数学成绩

        # 定义字段标签与控件的映射
        fields = [
            ("姓名：", self.nameInput),  # 姓名字段与对应的输入框
            ("性别：", self.genderCombo),  # 性别字段与对应的下拉框
            ("家庭：", self.familyCombo),  # 班级字段与对应的下拉框
            ("手机：", self.phoneInput),  # 语文字段与对应的输入框
            ("名字：", self.holyNameInput)  # 数学字段与对应的输入框
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


class StudentDialog(QWidget):  # 定义一个用于添加学生的弹窗类，继承自 BaseStudentDialog
    def __init__(self):  # 初始化方法，接收父窗口作为参数，默认为 None
        super().__init__()  # 调用父类的初始化方法，设置弹窗标题为“添加学生”，并传递父窗口
        self.setObjectName("StudentInterface")
        self.baseStudentFuncTemp_1 = BaseStudentFuncTemp()
        self.baseStudentFuncTemp_2 = BaseStudentFuncTemp()
        self.verticalLayout = QVBoxLayout(self)

        self.verticalLayout.addLayout(self.baseStudentFuncTemp_1.main_verticalLayout)
        self.verticalLayout.addLayout(self.baseStudentFuncTemp_2.main_verticalLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddStudentDialog()
    window.show()
    sys.exit(app.exec())
