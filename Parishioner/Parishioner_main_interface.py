from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from qfluentwidgets import (qrouter, TabBar, TabCloseButtonDisplayMode, FluentIcon)

from Parishioner.Parishioner_Interface import Parishioner_Main_Interface
from Parishioner.family_interface import Family_Main_Interface
from utils.custom_style import StyleSheet


# 该文件是人员信息主界面，此处添加和管理两个子界面，包括教友信息和家庭信息

class ParishionerMainInterface(QWidget):

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

        self.parishioner_interface = Parishioner_Main_Interface(self.login_info,
                                                                "Parishioner_Main_Interface_from_Main_Even")

        self.family_interface = Family_Main_Interface(self.login_info,
                                                      "Family_Main_Interface_from_Main_Even")

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.main_vBoxLayout.addWidget(self.tabView)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.addSubInterface(self.parishioner_interface,
                             'parishioner_interface', self.tr('教友信息'), FluentIcon.VIEW)
        self.addSubInterface(self.family_interface,
                             'family_interface', self.tr('家庭信息'), FluentIcon.ZOOM)

        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        qrouter.setDefaultRouteKey(self.stackedWidget, self.parishioner_interface.objectName())

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
