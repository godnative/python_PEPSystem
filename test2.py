import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit)
from PyQt6.QtGui import (QTextDocument, QFont, QTextCursor, QTextCharFormat,
                         QTextBlockFormat, QFontDatabase)
from PyQt6.QtPrintSupport import (QPrinter, QPrintDialog, QPrintPreviewDialog)
from datetime import datetime


class FormattedTextPrinter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口基本属性
        self.setWindowTitle('带格式文本打印器')
        self.setGeometry(100, 100, 800, 600)

        # 创建中心部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 人名输入区域
        name_layout = QHBoxLayout()
        name_label = QLabel('请输入人名:')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('在这里输入要插入的人名')
        update_btn = QPushButton('更新文本')
        update_btn.clicked.connect(self.update_text)

        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(update_btn)

        # 格式化文本框
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # 设置为只读，防止用户直接修改

        # 打印按钮
        print_btn = QPushButton('打印文本')
        print_btn.clicked.connect(self.show_print_preview)  # 改为显示预览

        # 添加部件到主布局
        main_layout.addLayout(name_layout)
        main_layout.addWidget(self.text_edit)
        main_layout.addWidget(print_btn)

        # 初始化文本内容
        self.update_text()

    def update_text(self):
        """更新文本框内容，应用指定的格式"""
        # 获取输入的人名，如果为空则使用默认值
        person_name = self.name_input.text().strip() or "张三"

        # 清空现有内容
        self.text_edit.clear()

        # 获取文本光标用于格式化
        cursor = self.text_edit.textCursor()

        # 1. 添加标题（居中）
        title_format = QTextBlockFormat()
        title_format.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # 水平居中

        char_format = QTextCharFormat()
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        char_format.setFont(title_font)

        cursor.setBlockFormat(title_format)
        cursor.setCharFormat(char_format)
        cursor.insertText("重要通知\n\n")

        # 2. 添加正文（开头空两格）
        body_format = QTextBlockFormat()
        body_format.setTextIndent(2 * self.text_edit.fontMetrics().horizontalAdvance(' '))  # 首行缩进两个字符

        body_font = QFont()
        body_font.setPointSize(12)
        char_format.setFont(body_font)
        char_format.setFontUnderline(False)  # 重置下划线格式

        cursor.setBlockFormat(body_format)
        cursor.setCharFormat(char_format)

        # 正文内容，分部分插入以对人名应用特殊格式
        cursor.insertText("根据最新安排，现邀请")

        # 对人名应用下划线格式
        name_format = QTextCharFormat(char_format)  # 复制当前格式
        name_format.setFontUnderline(True)  # 设置下划线
        cursor.setCharFormat(name_format)
        cursor.insertText(person_name)  # 插入带下划线的人名

        # 恢复正常格式继续插入文本
        cursor.setCharFormat(char_format)
        cursor.insertText("参加本周的项目会议。会议将讨论下一阶段的工作计划和目标，\n\n")

        # 继续插入其他正文内容
        cursor.insertText("请提前准备相关材料，并准时参加。如有特殊情况不能参加，请提前告知。\n\n")
        cursor.insertText("感谢您的配合与支持！\n\n")

        # 3. 添加落款（靠右）和时间
        signature_format = QTextBlockFormat()
        signature_format.setAlignment(Qt.AlignmentFlag.AlignRight)  # 靠右对齐

        cursor.setBlockFormat(signature_format)

        # 落款名称
        cursor.insertText("项目管理部\n")

        # 日期时间（当前时间）
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        cursor.insertText(current_time)

        # 确保文本框内容可见
        self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)

    def show_print_preview(self):
        """显示打印预览窗口"""
        # 创建打印机实例
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)

        # 创建打印预览对话框
        preview_dialog = QPrintPreviewDialog(printer, self)
        # 连接预览信号，设置绘制预览的回调函数
        preview_dialog.paintRequested.connect(self.print_preview)

        # 设置预览窗口标题和大小
        preview_dialog.setWindowTitle("打印预览")
        preview_dialog.resize(1000, 800)

        # 显示预览对话框
        preview_dialog.exec()

    def print_preview(self, printer):
        """打印预览回调函数，用于在预览窗口中绘制内容"""
        self.text_edit.document().print(printer)

    def print_text(self, printer=None):
        """实际执行打印操作"""
        if not printer:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            dialog = QPrintDialog(printer, self)

            if dialog.exec() != QPrintDialog.DialogCode.Accepted:
                return

        self.text_edit.document().print(printer)


if __name__ == '__main__':
    # 导入Qt需要放在这里以避免循环导入问题
    from PyQt6.QtCore import Qt

    app = QApplication(sys.argv)
    window = FormattedTextPrinter()
    window.show()
    sys.exit(app.exec())
