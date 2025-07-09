from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication
from qfluentwidgets import (qrouter, TabBar, TabCloseButtonDisplayMode)

from Event.ComEventMessageBoxBase import Event_Main_Interface
from utils.custom_style import StyleSheet


# 该文件是事件主界面，此处添加和管理三个子界面

class EvenMainTabInterface(QWidget):

    def __init__(self, login_info, ObjectName):
        super().__init__()
        self.login_info = login_info

        # 创建主布局
        self.setObjectName(ObjectName)

        self.tabCount = 1
        self.setObjectName(ObjectName)

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)

        self.tabBar.setMovable(False)
        self.tabBar.setScrollable(False)
        self.tabBar.setTabShadowEnabled(True)
        self.tabBar.addButton.hide()
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)

        self.main_vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)

        self.baptism_interface = Event_Main_Interface(
            self.login_info, "EventBaptism_Main_Interface_from_Main_Even", 1, self)
        self.confirmation_interface = Event_Main_Interface(
            self.login_info, "EventConfirmation_Main_Interface_from_Main_Even", 0, self)
        self.marriage_interface = Event_Main_Interface(
            self.login_info, "EventMarriage_Main_Interface_from_Main_Even", 2, self)

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.main_vBoxLayout.addWidget(self.tabView)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.addSubInterface(self.confirmation_interface,
                             'ConfirmationInterface', self.tr('坚振圣事'), ':/gallery/images/Dvd.png')
        self.addSubInterface(self.baptism_interface,
                             'baptismInterface', self.tr('圣洗圣事'), ':/gallery/images/MusicNote.png')
        self.addSubInterface(self.marriage_interface,
                             'marriageInterface', self.tr('婚姻圣事'), ':/gallery/images/Singer.png')

        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        qrouter.setDefaultRouteKey(self.stackedWidget, self.baptism_interface.objectName())

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def addSubInterface(self, widget, objectName, text, icon):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return

        self.tabBar.setCurrentTab(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login_info = {
        "parish_id": 1,
        "parish_name": "崇义教区",
        "user_id": 1,
        "user_name": "admin",
        "user_type": 1,
        "user_authnum": 32767
    }
    main_window = EvenMainTabInterface(login_info, "testParishioner_Main_Interface")
    main_window.show()
    main_window.resize(1000, 800)

    sys.exit(app.exec())