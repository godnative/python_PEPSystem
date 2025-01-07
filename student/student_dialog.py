# student/student_dialog.py文件中
from PyQt6.QtCore import Qt  # 导入 PyQt6 模块中的 Qt 类，用于对齐方式等常量
from PyQt6.QtWidgets import QGridLayout  # 导入 PyQt6 模块中的 QGridLayout，用于栅格布局
from qfluentwidgets import MessageBoxBase, ComboBox, LineEdit, StrongBodyLabel, \
    SubtitleLabel, InfoBar, PushButton  # 导入 qfluentwidgets 模块中的组件

from DataBase.family_db import FamilyDB
from student.family_dialog import AddFamilyDialog


class BaseStudentDialog(MessageBoxBase):  # 定义一个学生信息弹窗的基类，继承自 MessageBoxBase
    def __init__(self, title, parent):  # 初始化方法，接收弹窗标题和父窗口作为参数
        super().__init__(parent)  # 调用父类的初始化方法，设置父窗口
        self.title = title  # 保存弹窗标题，用于区分弹窗用途（如添加或修改学生信息）
        self.cur_school_id = 1
        self.role = parent.role
        self.school_info = parent.school_info
        self.family_info = None
        self.setup_ui()  # 调用界面设置方法，初始化弹窗界面
        self.load_family()  # 调用加载班级方法，为弹窗提供班级选择功能

    def setup_ui(self):  # 定义设置用户界面的方法
        self.titleLabel = SubtitleLabel(self.title, self)  # 创建一个 SubtitleLabel 实例，传入标题文本和父窗口
        self.viewLayout.addWidget(self.titleLabel)  # 将标题控件添加到布局中
        self.viewLayout.setAlignment(self.titleLabel, Qt.AlignmentFlag.AlignCenter)  # 设置标题控件在布局中的对齐方式为居中

        self.grid_layout = QGridLayout()  # 创建一个栅格布局对象，用于对控件进行行列排布
        self.viewLayout.addLayout(self.grid_layout)  # 将栅格布局添加到主视图布局中

        # 创建输入控件
        self.nameInput = LineEdit(self)  # 创建一个单行文本输入框用于输入姓名
        self.genderCombo = ComboBox(self)  # 创建一个下拉框组件用于选择性别
        self.genderCombo.addItem("男", userData=0)
        self.genderCombo.addItem("女", userData=1)
        self.familyCombo = ComboBox(self)  # 创建一个下拉框组件用于选择班级
        self.phoneInput = LineEdit(self)  # 创建一个单行文本输入框用于输入语文成绩
        self.holyNameInput = LineEdit(self)  # 创建一个单行文本输入框用于输入数学成绩

        # 定义字段标签与控件的映射
        fields = [
            ("姓名：", self.nameInput),  # 姓名字段与对应的输入框
            ("性别：", self.genderCombo),  # 性别字段与对应的下拉框
            ("手机：", self.phoneInput),  # 语文字段与对应的输入框
            ("名字：", self.holyNameInput),  # 数学字段与对应的输入框
            ("家庭：", self.familyCombo),  # 班级字段与对应的下拉框
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
        for widget in [self.nameInput, self.genderCombo, self.familyCombo, self.phoneInput,
                       self.holyNameInput]:
            widget.setMinimumWidth(200)  # 为每个输入框设置最小宽度为 200

        # 将焦点定位到姓名输入框
        self.nameInput.setFocus()  # 设置焦点到姓名输入框，使其在弹出时默认获取焦点

        # 确保“确定”按钮不会自动对焦
        self.yesButton.setDefault(False)  # 取消“确定”按钮的默认焦点
        self.yesButton.setAutoDefault(False)  # 禁止“确定”按钮自动成为默认按钮

    # 定义一个方法 load_classes，用于加载班级信息到下拉框中
    def load_family(self):
        self.familyCombo.clear()  # 清空 classCombo 下拉框中的所有选项
        with FamilyDB() as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            self.family_info = db.fetch_family()  # 如果没有可管理的班级 ID 列表，则获取所有班级信息
        self.familyCombo.addItem('请选择班级', None)  # 在下拉框中添加默认选项 "请选择班级"，并将其关联的数据设为 None

        for family_info in self.family_info:  # 遍历获取到的班级信息列表
            self.familyCombo.addItem(family_info['family_name'],
                                     userData=family_info['family_id'])  # 将每个班级的名称和对应的 ID 添加到下拉框中

    # 验证用户输入的所有字段
    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.nameInput.text().strip():
            errors.append("请输入姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.phoneInput.text().strip():
            errors.append("请输入学号")  # 验证学号是否填写，如果未填写，添加错误信息

        if self.familyCombo.currentData() is None:
            errors.append("请选择班级")  # 验证班级是否选择，如果未选择班级，添加错误信息

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

    def get_InputStudentDialoginfo(self):
        StudentInfo = {
            "student_name": self.nameInput.text(),
            "student_gender": self.genderCombo.currentData(),
            "student_phonenum": self.phoneInput.text(),  # 性别字段与对应的下拉框
            "student_holyname": self.holyNameInput.text(),  # 班级字段与对应的下拉框
            "student_family_id": self.familyCombo.currentData(),  # 语文字段与对应的输入框
            "student_school_id": self.school_info["school_id"]  # 语文字段与对应的输入框
        }
        return StudentInfo

    def set_InputStudentDialoginfo(self, StudentInfo):
        self.nameInput.setText(StudentInfo["student_name"])
        self.genderCombo.setCurrentIndex(StudentInfo["student_gender"])
        self.phoneInput.setText(StudentInfo["student_phonenum"])
        self.holyNameInput.setText(StudentInfo["student_holyname"])
        family_idx = self.familyCombo.findData(StudentInfo["student_family_id"])
        self.familyCombo.setCurrentIndex(family_idx)
        return StudentInfo


class AddStudentDialog(BaseStudentDialog):  # 定义一个用于添加学生的弹窗类，继承自 BaseStudentDialog
    def __init__(self, parent):  # 初始化方法，接收父窗口作为参数，默认为 None
        super().__init__('添加学生', parent)  # 调用父类的初始化方法，设置弹窗标题为“添加学生”，并传递父窗口
        self.role = parent.role
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能
        self.add_family_pushbutton = PushButton("新增家庭", self)
        self.grid_layout.addWidget(self.add_family_pushbutton, 5, 1)
        self.add_family_pushbutton.clicked.connect(self.add_family)

    def add_family(self):
        w = AddFamilyDialog(self)
        if w.exec():
            print(w.get_InputFamilyDialoginfo())
            with FamilyDB() as db:
                db.add_family(w.get_InputFamilyDialoginfo())
            self.load_family()


class ModifyStudentDialog(BaseStudentDialog):  # 定义一个用于添加学生的弹窗类，继承自 BaseStudentDialog
    def __init__(self, parent):  # 初始化方法，接收父窗口作为参数，默认为 None
        super().__init__('修改学生', parent)  # 调用父类的初始化方法，设置弹窗标题为“添加学生”，并传递父窗口
        self.yesButton.setText('确认')  # 设置确认按钮的文本为“添加”，以明确功能


class DelStudentDialog(BaseStudentDialog):  # 定义一个用于添加学生的弹窗类，继承自 BaseStudentDialog
    def __init__(self, parent):  # 初始化方法，接收父窗口作为参数，默认为 None
        super().__init__('确认删除学生？', parent)  # 调用父类的初始化方法，设置弹窗标题为“添加学生”，并传递父窗口
        self.yesButton.setText('确认删除')  # 设置确认按钮的文本为“添加”，以明确功能
