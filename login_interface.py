import os
import pickle
import sys

from PyQt6.QtCore import QRect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from PyQt6.QtWidgets import QMessageBox
from qfluentwidgets import FluentIcon as FIF, InfoBadge, InfoBadgePosition
from qfluentwidgets import (NavigationItemPosition, MSFluentWindow,
                            SubtitleLabel, setFont)
from qfluentwidgets import setThemeColor, SplitTitleBar
from qframelesswindow import AcrylicWindow as Window

from BaseWidgets.BaseModule import user_type
from DataBase.parish_db import ParishDb
from DataBase.user_db import UserDB
from Event.EvenMainTabInterface import EvenMainTabInterface
from LoginWindow import Ui_Form
from Parishioner.Parishioner_main_interface import ParishionerMainInterface
from TaskCard.TaskCardMainInterface import TaskCardMainInterFace
from school.school_interface import ShowSchoolInterface
from user.user_main_interface import UserMainInterface


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

        self.cur_login_parish_info = None
        self.comboBox.currentIndexChanged.connect(self.set_cur_login_parish_info)
        self.last_login_info_path = "./login_info.pkl"

        # self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())

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
        ww, hh = desktop.width(), desktop.height()
        self.move(ww // 2 - self.width() // 2, hh // 2 - self.height() // 2)

        # self.lineEdit_3.setText("admin")
        # self.lineEdit_5.setText("admin123")
        self.pushButton.clicked.connect(self.login)
        self.load_all_parish()
        self.load_last_login_info()

    def systemTitleBarRect(self, size):
        """ Returns the system title bar rect, only works for macOS """
        return QRect(size.width() - 75, 0, 75, size.height())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap("./resource/pic/background.jpg").scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)
        self.label_2.setPixmap(QPixmap("./login/resource/images/logo.png"))

    def load_all_parish(self):
        self.comboBox.clear()  # 清空 classCombo 下拉框中的所有选项
        test = ParishDb()
        test.connect_to_mysql_and_create_db()
        test.creat_all_database()
        with ParishDb() as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            load_parish_info = db.fetch_parish()
        self.comboBox.addItem('请选择教区', None)

        if load_parish_info is not None:
            for parish_info in load_parish_info:
                self.comboBox.addItem(parish_info['parish_name'],
                                      userData=parish_info)

    def set_cur_login_parish_info(self):
        self.cur_login_parish_info = self.comboBox.currentData()

    def save_last_login_info(self, login_info):
        with open(self.last_login_info_path, 'wb') as f:
            pickle.dump(login_info, f)

    def login(self):
        username = self.lineEdit_3.text()
        password = self.lineEdit_5.text()

        with UserDB() as db:
            user_info = db.user_login_check(username, password)

        if user_info is not None:
            login_info = {
                "parish_id": None,
                "parish_name": None,
                "user_id": None,
                "user_name": None,
                "user_type": None,
                "user_authnum": None
            }
            if self.cur_login_parish_info is not None:
                login_info["parish_id"] = self.cur_login_parish_info["parish_id"]
                login_info["parish_name"] = self.cur_login_parish_info["parish_name"]
            login_info["user_id"] = user_info["user_id"]
            login_info["user_name"] = user_info["user_name"]
            login_info["user_type"] = user_info["user_type"]
            login_info["user_authnum"] = user_info["user_authnum"]

            if self.checkBox.isChecked():
                with open(self.last_login_info_path, 'wb') as f:
                    save_login_info = {
                        "parish_id": login_info["parish_id"],
                        "user_name": username,
                        "user_password": password
                    }
                    pickle.dump(save_login_info, f)
            else:
                if os.path.exists(self.last_login_info_path):
                    os.remove(self.last_login_info_path)
            self.close()

            mainwindow = MainWindow(login_info)
            mainwindow.show()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')

    def load_last_login_info(self):
        if os.path.exists(self.last_login_info_path):
            with open(self.last_login_info_path, 'rb') as f:
                data = pickle.load(f)
                if data is not None:
                    all_parish_id = data['parish_id']
                    if all_parish_id is not None and self.comboBox.count() > 1:
                        for i in range(self.comboBox.count()):
                            parish_info = self.comboBox.itemData(i)
                            if parish_info is None:
                                continue
                            if all_parish_id == parish_info["parish_id"]:
                                self.comboBox.setCurrentIndex(i)
                                break
                    if data.get('user_name') is not None and data.get('user_password') is not None:
                        self.lineEdit_3.setText(data['user_name'])
                        self.lineEdit_5.setText(data['user_password'])


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(MSFluentWindow):
    def __init__(self, login_info):
        super().__init__()
        self.login_info = login_info
        self.schoolInterface = ShowSchoolInterface(self.login_info, "ShowSchoolInterface")
        if self.login_info["parish_id"] is None:
            self.setWindowTitle('未选择当前教区')
            self.addSubInterface(self.schoolInterface, FIF.APPLICATION, '教区')
        else:
            self.setWindowTitle(
                '当前教区:%s  当前登录角色：%s' % (self.login_info['parish_name'] , user_type[self.login_info['user_type']]))
            # create sub interface
            self.studentInterface = ParishionerMainInterface(self.login_info, "Parishioner_Main_Interface")
            self.videoInterface = EvenMainTabInterface(self.login_info, "EvenMainTabInterface")
            self.libraryInterface = UserMainInterface(self.login_info, "UserMainInterface")
            self.taskCardInterface = TaskCardMainInterFace(self.login_info, "TaskCardMainInterFace")

            self.addSubInterface(self.schoolInterface, FIF.APPLICATION, '教区')
            self.addSubInterface(self.studentInterface, FIF.HOME, '教友')
            self.addSubInterface(self.videoInterface, FIF.VIDEO, '圣事')

            self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '资料', FIF.LIBRARY_FILL,
                                 NavigationItemPosition.BOTTOM)
            self.addSubInterface(self.taskCardInterface, FIF.BOOK_SHELF, '通知', FIF.LIBRARY_FILL,
                                 NavigationItemPosition.BOTTOM)

            self.navigationInterface.setCurrentItem(self.schoolInterface.objectName())

            self.taskCardInterface.taskcardwaitfinishnumchanged.connect(self.setTaskCardWaitFinishNumber)

        self.initWindow()

    def initWindow(self):
        self.resize(1500, 1000)
        self.setWindowIcon(QIcon('./login/resource/images/logo.png'))

        desktop = QApplication.screens()[0].availableGeometry()
        ww, hh = desktop.width(), desktop.height()
        self.move(ww // 2 - self.width() // 2, hh // 2 - self.height() // 2)

    def on_back_to_login(self):
        self.close()
        login_window = LoginWindow()
        login_window.show()

    def setTaskCardWaitFinishNumber(self, num):
        # add badge to navigation item
        item = self.navigationInterface.widget(self.taskCardInterface.objectName())
        InfoBadge.attension(
            text=str(num),
            parent=item.parent(),
            target=item,
            position=InfoBadgePosition.NAVIGATION_ITEM
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = LoginWindow()
    w.show()
    app.exec()
