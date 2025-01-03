from PyQt6.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import (qrouter, TabBar, TabCloseButtonDisplayMode)

from HolyEvent.holyevent_dialog import HolyEventBaptismInterFace
from utils.custom_style import StyleSheet


class HolyEvenTabInterface(QWidget):

    def __init__(self, curSchool, parent=None):
        super().__init__(parent=parent)
        self.tabCount = 1
        self.setObjectName("HolyEvenTabInterface")
        self.curSchool = curSchool
        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)

        self.tabBar.setMovable(False)
        self.tabBar.setScrollable(False)
        self.tabBar.setTabShadowEnabled(True)
        self.tabBar.addButton.hide()
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)

        self.baptism_interface = HolyEventBaptismInterFace(self.curSchool)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('Artist Interface', self)

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.addSubInterface(self.baptism_interface,
                             'baptismInterface', self.tr('圣洗圣事'), ':/gallery/images/MusicNote.png')
        self.addSubInterface(self.albumInterface,
                             'tabAlbumInterface', self.tr('Album'), ':/gallery/images/Dvd.png')
        self.addSubInterface(self.artistInterface,
                             'tabArtistInterface', self.tr('Artist'), ':/gallery/images/Singer.png')

        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.connectSignalToSlot()

        qrouter.setDefaultRouteKey(
            self.stackedWidget, self.baptism_interface.objectName())

    def connectSignalToSlot(self):
        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def initLayout(self):
        self.hBoxLayout.addWidget(self.tabView, 1)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)

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
