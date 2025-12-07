import os
import pickle
import sys
from logging.handlers import RotatingFileHandler

from deceased_parishioner.deceased_parishioner_interface import Deceased_Parishioner_Main_Interface
from parish.parish_interface_new import Parish_Main_Interface
from utils.msyscfg import CUR_SYS_TYPE

from PyQt6.QtCore import QRect # type: ignore
from PyQt6.QtCore import Qt # pyright: ignore[reportMissingImports]
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
from setting.settingMainInterFace import SettingMainInterFace
from user.user_main_interface import UserMainInterface

import traceback
import logging
from PyQt6.QtCore import QtMsgType, qInstallMessageHandler


# 1. 设置日志
def setup_logging():
    # 创建 logger 对象（可选，默认使用 root logger）
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 定义日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 创建 RotatingFileHandler（设置最大 5MB，保留 3 个备份）
    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,  # 保留 3 个旧日志
        encoding='utf-8'  # 可选：设置编码
    )
    file_handler.setFormatter(formatter)

    # 创建 StreamHandler（输出到控制台）
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # 移除默认的 handlers（避免重复日志）
    logger.handlers.clear()

    # 添加自定义 handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


# 2. 全局异常处理
def handle_exception(exc_type, exc_value, exc_traceback):
    error = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.error(f"未捕获异常:\n{error}")
    if QApplication.instance():
        QMessageBox.critical(None, "错误", "程序崩溃，请查看日志文件。")
    sys.exit(1)


# 3. Qt 消息处理
def qt_message_handler(mode, context, message):
    if mode == QtMsgType.QtDebugMsg:
        logging.debug(f"Qt: {message}")
    elif mode == QtMsgType.QtWarningMsg:
        logging.warning(f"Qt: {message}")
    else:
        logging.error(f"Qt: {message}")


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
        if CUR_SYS_TYPE == 0:
            db = ParishDb(self)
            db.creat_all_database()
        self.load_all_parish()
        self.load_last_login_info()

    def systemTitleBarRect(self, size):
        """ Returns the system title bar rect, only works for macOS """
        return QRect(size.width() - 75, 0, 75, size.height())

    def resizeEvent(self, even):
        super().resizeEvent(even)
        pixmap = QPixmap("./resource/pic/background.jpg").scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)
        self.label_2.setPixmap(QPixmap("./login/resource/images/logo.png"))

    def load_all_parish(self):
        with ParishDb(self) as db:  # 使用上下文管理器创建 ClassDB 的实例，并确保使用后自动关闭数据库连接
            load_parish_info = db.fetch_parish()
            if not load_parish_info:
                self.comboBox.setDisabled(True)
        self.comboBox.addItem('请选择堂区', None)

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

        with UserDB(self) as db:
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
            mainwindow.resize(1200,800)
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
        print(login_info)
        self.login_info = login_info
        self.schoolInterface = Parish_Main_Interface(self.login_info, "ShowSchoolInterface")
        if self.login_info["parish_id"] is None:
            self.setWindowTitle('未选择当前堂区')
            self.addSubInterface(self.schoolInterface, FIF.APPLICATION, '堂区')
        else:
            self.setWindowTitle(
                '当前堂区:%s  当前登录角色：%s' % (
                    self.login_info['parish_name'], user_type[self.login_info['user_type']]))
            # create sub interface
            self.studentInterface = ParishionerMainInterface(self.login_info, "Parishioner_Main_Interface")
            self.videoInterface = EvenMainTabInterface(self.login_info, "EvenMainTabInterface")
            self.libraryInterface = UserMainInterface(self.login_info, "UserMainInterface")
            self.taskCardInterface = TaskCardMainInterFace(self.login_info, "TaskCardMainInterFace")
            self.deadInterface = Deceased_Parishioner_Main_Interface(self.login_info, "DeceasedParishionerInterface")

            self.addSubInterface(self.schoolInterface, FIF.APPLICATION, '堂区')
            self.addSubInterface(self.studentInterface, FIF.PEOPLE, '教友')
            self.addSubInterface(self.videoInterface, FIF.VIDEO, '圣事')
            self.addSubInterface(self.deadInterface, FIF.HOME_FILL, '亡者')

            self.addSubInterface(self.libraryInterface, FIF.BOOK_SHELF, '资料')
            self.addSubInterface(self.taskCardInterface, FIF.PHONE, '通知')

            if self.login_info["user_type"] == 0:
                self.settingInterface = SettingMainInterFace("SettingMainInterFace")
                self.addSubInterface(self.settingInterface, FIF.SETTING, '设置', FIF.LIBRARY_FILL,
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
    # 设置异常处理
    sys.excepthook = handle_exception

    # 设置日志
    setup_logging()

    # 设置Qt消息处理
    qInstallMessageHandler(qt_message_handler)

    try:
        app = QApplication(sys.argv)
        window = LoginWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.error("主程序异常", exc_info=True)
        QMessageBox.critical(None, "启动失败", f"程序启动失败: {str(e)}")
        sys.exit(1)
