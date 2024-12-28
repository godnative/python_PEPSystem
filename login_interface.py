import sys

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox
from qfluentwidgets import setThemeColor, SplitTitleBar, isDarkTheme
from qframelesswindow import AcrylicWindow as Window

from DataBase.school_db import SchoolDb
from DataBase.user_db import UserDB
from LoginWindow import Ui_Form
from main_window import MainWindow


class LoginWindow(Window, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('PyQt-Fluent-Widget')
        self.setWindowIcon(QIcon("./login/resource/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())

        if sys.platform == "darwin":
            self.setSystemTitleBarButtonVisible(True)
            self.titleBar.minBtn.hide()
            self.titleBar.maxBtn.hide()
            self.titleBar.closeBtn.hide()

        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.lineEdit_3.setText("admin")
        self.lineEdit_5.setText("password")
        self.pushButton.clicked.connect(self.login)
        self.load_schools()

    def systemTitleBarRect(self, size):
        """ Returns the system title bar rect, only works for macOS """
        return QRect(size.width() - 75, 0, 75, size.height())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap("./login/resource/images/background.jpg").scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)
        self.label_2.setPixmap(QPixmap("./login/resource/images/logo.png"))

    def login(self):
        username = self.lineEdit_3.text()
        password = self.lineEdit_5.text()

        with UserDB() as db:
            user_info = db.user_login_check(username, password)

        if user_info is not None:
            self.close()
            mainWindow = MainWindow(user_info, self.comboBox.currentData())
            mainWindow.show()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')

    def load_schools(self):
        self.comboBox.clear()  # 清空 classCombo 下拉框中的所有选项
        with SchoolDb() as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            schools = db.fetch_school()  # 如果没有可管理的班级 ID 列表，则获取所有班级信息
        self.comboBox.addItem('请选择学校', None)  # 在下拉框中添加默认选项 "请选择班级"，并将其关联的数据设为 None

        for school_info in schools:  # 遍历获取到的班级信息列表
            self.comboBox.addItem(school_info['school_name'],
                                  userData=school_info['school_id'])  # 将每个班级的名称和对应的 ID 添加到下拉框中


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    app.exec()
