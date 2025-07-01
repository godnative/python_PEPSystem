import sys

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel,
    QLineEdit, QPushButton, QVBoxLayout,
    QWidget, QMessageBox, QDateEdit
)

from DataBase.parish_db import ParishDb


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口标题和大小
        self.setWindowTitle("简单的PyQt6应用")
        self.setGeometry(100, 100, 400, 300)

        # 创建主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建界面元素
        self.label = QLabel("请输入内容:")
        self.input = QLineEdit()
        self.button = QPushButton("点击我")
        dateedit = QDateEdit()
        with ParishDb() as db:
            date = db.get_parish_info(1)['parish_date']

        dateedit.setDate(date)

        # 将元素添加到布局
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.addWidget(dateedit)

        # 连接按钮点击信号到槽函数
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # 获取输入框内容并显示
        text = self.input.text()
        if text:
            QMessageBox.information(self, "你输入了", f"你输入的内容是: {text}")
        else:
            QMessageBox.warning(self, "警告", "输入框不能为空!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())