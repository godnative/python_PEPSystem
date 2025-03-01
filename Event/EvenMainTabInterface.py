from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from qfluentwidgets import (qrouter, TabBar, TabCloseButtonDisplayMode)

from Event.EvenConfirmationInterface import EventConfirmation_Main_Interface
from Event.EvenMarriageInterface import EventMarriage_Main_Interface
from Event.EventBaptismInterFace import EventBaptism_Main_Interface
from utils.custom_style import StyleSheet


class EvenMainTabInterface(QWidget):

    def __init__(self, cur_parish, cur_user, ObjectName):
        super().__init__()

        # 创建主布局
        self.setObjectName(ObjectName)
        self.cur_parish = cur_parish
        self.cur_user = cur_user

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

        self.baptism_interface = EventBaptism_Main_Interface(self.cur_parish, self.cur_user,
                                                             "EventBaptism_Main_Interface_from_Main_Even", self)

        self.confirmation_interface = EventConfirmation_Main_Interface(
            self.cur_parish, self.cur_user, "EventConfirmation_Main_Interface_from_Main_Even", self)
        self.marriage_interface = EventMarriage_Main_Interface(self.cur_parish, self.cur_user,
                                                               "EventMarriage_Main_Interface_from_Main_Even")

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.main_vBoxLayout.addWidget(self.tabView)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.addSubInterface(self.baptism_interface,
                             'baptismInterface', self.tr('圣洗圣事'), ':/gallery/images/MusicNote.png')
        self.addSubInterface(self.confirmation_interface,
                             'ConfirmationInterface', self.tr('坚振圣事'), ':/gallery/images/Dvd.png')
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
