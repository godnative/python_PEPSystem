from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from qfluentwidgets import TabBar, TabCloseButtonDisplayMode, qrouter

from user.User_Interface import User_Show_Interface, User_Modify_Interface
from utils.custom_style import StyleSheet


class UserMainInterface(QWidget):

    def __init__(self, login_info, ObjectName):
        super().__init__()
        self.login_info = login_info
        # 创建主布局
        self.setObjectName(ObjectName)

        self.tabCount = 1
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

        self.user_show_interface = User_Show_Interface(
            self.login_info, "User_Show_Interface_from_Main_Even")

        self.user_modify_interface = User_Modify_Interface("User_Modify_Interface_from_Main_Even")

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.main_vBoxLayout.addWidget(self.tabView)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.addSubInterface(
            self.user_show_interface, 'user_show_interface', self.tr('当前用户信息'), ':/gallery/images/MusicNote.png')
        if self.login_info["user_type"] == 0:
            self.addSubInterface(
                self.user_modify_interface, 'user_modify_interface', self.tr('修改用户信息'), ':/gallery/images/Dvd.png')

        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        qrouter.setDefaultRouteKey(self.stackedWidget, self.user_show_interface.objectName())

        # noinspection PyUnresolvedReferences
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
