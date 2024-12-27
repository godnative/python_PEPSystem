# student/student_dialog.py文件中
from PyQt6.QtCore import Qt  # 导入 PyQt6 模块中的 Qt 类，用于对齐方式等常量
from PyQt6.QtWidgets import QGridLayout  # 导入 PyQt6 模块中的 QGridLayout，用于栅格布局
from qfluentwidgets import MessageBoxBase, ComboBox, LineEdit, StrongBodyLabel, \
    SubtitleLabel, InfoBar  # 导入 qfluentwidgets 模块中的组件

from DataBase.classes_db import ClassDB  # 从数据库模块 classes_db 中导入 ClassDB 类，用于处理班级相关的数据库操作


class BaseStudentDialog(MessageBoxBase):  # 定义一个学生信息弹窗的基类，继承自 MessageBoxBase
    def __init__(self, title, parent=None):  # 初始化方法，接收弹窗标题和父窗口作为参数
        super().__init__(parent)  # 调用父类的初始化方法，设置父窗口
        self.title = title  # 保存弹窗标题，用于区分弹窗用途（如添加或修改学生信息）
        self.setup_ui()  # 调用界面设置方法，初始化弹窗界面
        self.load_classes()  # 调用加载班级方法，为弹窗提供班级选择功能

    def setup_ui(self):  # 定义设置用户界面的方法
        self.titleLabel = SubtitleLabel(self.title, self)  # 创建一个 SubtitleLabel 实例，传入标题文本和父窗口
        self.viewLayout.addWidget(self.titleLabel)  # 将标题控件添加到布局中
        self.viewLayout.setAlignment(self.titleLabel, Qt.AlignmentFlag.AlignCenter)  # 设置标题控件在布局中的对齐方式为居中

        grid_layout = QGridLayout()  # 创建一个栅格布局对象，用于对控件进行行列排布
        self.viewLayout.addLayout(grid_layout)  # 将栅格布局添加到主视图布局中

        # 创建输入控件
        self.nameInput = LineEdit(self)  # 创建一个单行文本输入框用于输入姓名
        self.numberInput = LineEdit(self)  # 创建一个单行文本输入框用于输入学号
        self.genderCombo = ComboBox(self)  # 创建一个下拉框组件用于选择性别
        self.genderCombo.addItems(['男', '女'])  # 为下拉框添加两个选项：男和女
        self.classCombo = ComboBox(self)  # 创建一个下拉框组件用于选择班级
        self.chineseInput = LineEdit(self)  # 创建一个单行文本输入框用于输入语文成绩
        self.mathInput = LineEdit(self)  # 创建一个单行文本输入框用于输入数学成绩
        self.englishInput = LineEdit(self)  # 创建一个单行文本输入框用于输入英语成绩

        # 定义字段标签与控件的映射
        fields = [
            ("姓名：", self.nameInput),  # 姓名字段与对应的输入框
            ("学号：", self.numberInput),  # 学号字段与对应的输入框
            ("性别：", self.genderCombo),  # 性别字段与对应的下拉框
            ("班级：", self.classCombo),  # 班级字段与对应的下拉框
            ("语文：", self.chineseInput),  # 语文字段与对应的输入框
            ("数学：", self.mathInput),  # 数学字段与对应的输入框
            ("英语：", self.englishInput)  # 英语字段与对应的输入框
        ]

        # 遍历字段，添加到栅格布局中
        for row, (label_text, widget) in enumerate(fields):  # 使用 enumerate 获取字段的行号
            label = StrongBodyLabel(label_text, self)  # 创建加粗的标签
            grid_layout.addWidget(label, row, 0)  # 将标签添加到栅格布局的第一列
            grid_layout.addWidget(widget, row, 1)  # 将控件添加到栅格布局的第二列

        # 设置列拉伸
        grid_layout.setColumnStretch(1, 1)  # 设置第二列的列拉伸系数为 1，确保控件能够自动适应窗口大小

        # 设置标签对齐方式
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # 将控件对齐到左侧

        # 修改按钮文本
        self.yesButton.setText('确定')  # 将确认按钮文本设置为“确定”
        self.cancelButton.setText('取消')  # 将取消按钮文本设置为“取消”

        # 设置输入框的宽度
        for widget in [self.nameInput, self.numberInput, self.genderCombo, self.classCombo,
                       self.chineseInput, self.mathInput, self.englishInput]:
            widget.setMinimumWidth(200)  # 为每个输入框设置最小宽度为 200

        # 将焦点定位到姓名输入框
        self.nameInput.setFocus()  # 设置焦点到姓名输入框，使其在弹出时默认获取焦点

        # 确保“确定”按钮不会自动对焦
        self.yesButton.setDefault(False)  # 取消“确定”按钮的默认焦点
        self.yesButton.setAutoDefault(False)  # 禁止“确定”按钮自动成为默认按钮

    # 定义一个方法 load_classes，用于加载班级信息到下拉框中
    def load_classes(self):
        self.classCombo.clear()  # 清空 classCombo 下拉框中的所有选项
        with ClassDB() as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            classes = db.fetch_classes()  # 如果没有可管理的班级 ID 列表，则获取所有班级信息
        self.classCombo.addItem('请选择班级', None)  # 在下拉框中添加默认选项 "请选择班级"，并将其关联的数据设为 None

        for class_info in classes:  # 遍历获取到的班级信息列表
            self.classCombo.addItem(class_info['class_name'],
                                    userData=class_info['class_id'])  # 将每个班级的名称和对应的 ID 添加到下拉框中

    # 验证分数是否在0到100之间
    def _validate_score(self, score):
        try:
            return 0 <= float(score) <= 100  # 尝试将分数转换为浮点数，并检查是否在0到100之间
        except ValueError:
            return False  # 如果分数无法转换为浮点数（如为空或非数字），返回False

    # 验证用户输入的所有字段
    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.nameInput.text().strip():
            errors.append("请输入学生姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.numberInput.text().strip():
            errors.append("请输入学号")  # 验证学号是否填写，如果未填写，添加错误信息

        if self.classCombo.currentData() is None:
            errors.append("请选择班级")  # 验证班级是否选择，如果未选择班级，添加错误信息

        for subject, input_field in [("语文", self.chineseInput),
                                     ("数学", self.mathInput),
                                     ("英语", self.englishInput)]:
            score = input_field.text()  # 获取分数输入框的文本内容
            if not self._validate_score(score):
                errors.append(f"{subject}分数必须是0-100之间")  # 如果分数不在0到100之间，添加对应科目的错误信息
        return errors   # 返回所有错误信息

    def accept(self):
        # 对数据进行验证
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self, duration=3000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return  # 返回以阻止继续执行
        # 如果验证通过，调用父类的 accept 方法，接收数据并关闭对话框
        super().accept()

    def get_InputStudentDialoginfo(self):
        StudentInfo = {
            "student_name": self.nameInput.text(),
            "student_number": self.numberInput.text(),
            "gender": self.genderCombo.currentIndex() + 1,  # 性别字段与对应的下拉框
            "class_id": self.classCombo.currentIndex(),  # 班级字段与对应的下拉框
            "chinese_score": float(self.chineseInput.text()),  # 语文字段与对应的输入框
            "math_score": float(self.mathInput.text()),  # 数学字段与对应的输入框
            "english_score": float(self.englishInput.text())
        }
        return StudentInfo


class AddStudentDialog(BaseStudentDialog):  # 定义一个用于添加学生的弹窗类，继承自 BaseStudentDialog
    def __init__(self, parent=None):  # 初始化方法，接收父窗口作为参数，默认为 None
        super().__init__('添加学生', parent)  # 调用父类的初始化方法，设置弹窗标题为“添加学生”，并传递父窗口
        self.student_id = None  # 初始化学生 ID 属性，默认为 None，表示新建学生时不需要指定 ID
        self.yesButton.setText('添加')  # 设置确认按钮的文本为“添加”，以明确功能