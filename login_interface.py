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

from DataBase.school_db import SchoolDb
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
        self.load_schools_and_user()

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

    def login(self):
        username = self.lineEdit_3.text()
        password = self.lineEdit_5.text()

        with UserDB() as db:
            user_info = db.user_login_check(username, password)

        if user_info is not None:
            if self.checkBox.isChecked():
                with open("./schoolsetting.pkl", 'wb') as f:
                    save_data = {
                        'school': self.comboBox.currentData(),
                        'user': user_info
                    }
                    pickle.dump(save_data, f)
            else:
                if os.path.exists('./schoolsetting.pkl'):
                    os.remove('./schoolsetting.pkl')
            self.close()
            mainwindow = MainWindow(user_info, self.comboBox.currentData())
            mainwindow.show()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')

    def load_schools_and_user(self):
        self.comboBox.clear()  # 清空 classCombo 下拉框中的所有选项
        with SchoolDb() as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            schools = db.fetch_school()  # 如果没有可管理的班级 ID 列表，则获取所有班级信息
        self.comboBox.addItem('请选择教区', None)  # 在下拉框中添加默认选项 "请选择班级"，并将其关联的数据设为 None

        for school_info in schools:  # 遍历获取到的班级信息列表
            self.comboBox.addItem(school_info['school_name'],
                                  userData=school_info)  # 将每个班级的名称和对应的 ID 添加到下拉框中

        if os.path.exists('./schoolsetting.pkl'):
            with open('./schoolsetting.pkl', 'rb') as f:
                data = pickle.load(f)
                if data is not None:
                    schoolinfo = data['school']
                    for school_info in schools:
                        if school_info['school_id'] == schoolinfo['school_id']:
                            self.comboBox.setCurrentIndex(self.comboBox.findData(school_info))
                            break
                    userinfo = data['user']
                    if userinfo['user_name'] is not None:
                        self.lineEdit_3.setText(userinfo['user_name'])
                        self.lineEdit_5.setText(userinfo['user_password'])


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

    def __init__(self, role, school_info):
        super().__init__()
        self.role = role
        self.school_info = school_info
        self.schoolInterface = ShowSchoolInterface(self)
        if self.school_info is None:
            self.setWindowTitle('未选择当前教区')
            self.studentInterface = Widget('请先选择教区', self)
            self.videoInterface = Widget('请先选择教区.', self)
            self.libraryInterface = Widget('请先选择教区..', self)
            self.echoInterface = Widget('请先选择教区...', self)
        else:
            self.setWindowTitle('当前教区:%s' % self.school_info['school_name'])
            # create sub interface
            self.studentInterface = ParishionerMainInterface(self.school_info, self.role, "Parishioner_Main_Interface")
            self.videoInterface = EvenMainTabInterface(self.school_info, self.role, "EvenMainTabInterface")
            self.libraryInterface = UserMainInterface(self.school_info, self.role, "UserMainInterface")
            self.taskCardInterface = TaskCardMainInterFace(self.school_info, "TaskCardMainInterFace")

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.schoolInterface, FIF.APPLICATION, '教区')
        self.addSubInterface(self.studentInterface, FIF.HOME, '教友')
        self.addSubInterface(self.videoInterface, FIF.VIDEO, '圣事')

        self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '资料', FIF.LIBRARY_FILL,
                             NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.taskCardInterface, FIF.BOOK_SHELF, '通知', FIF.LIBRARY_FILL,
                             NavigationItemPosition.BOTTOM)

        self.navigationInterface.setCurrentItem(self.schoolInterface.objectName())

        self.taskCardInterface.taskcardwaitfinishnumchanged.connect(self.setTaskCardWaitFinishNumber)

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
