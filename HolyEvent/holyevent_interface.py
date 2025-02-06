from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel
from qfluentwidgets import (qrouter, TabBar, TabCloseButtonDisplayMode)

from HolyEvent.holyevent_dialog import HolyEventBaptismInterFace
from student.stduent_basetemp import Student_Widget
from utils.custom_style import StyleSheet


class HolyEvenTabInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tabCount = 1
        self.setObjectName("HolyEvenTabInterface")
        self.role = parent.role
        self.school_info = parent.school_info
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

        self.baptism_interface = HolyEventBaptismInterFace(self)
        self.student_widget = Student_Widget(self)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('Artist Interface', self)

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.main_vBoxLayout.addWidget(self.tabView)
        self.main_vBoxLayout.addWidget(self.student_widget)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.addSubInterface(self.baptism_interface,
                             'baptismInterface', self.tr('圣洗圣事'), ':/gallery/images/MusicNote.png')
        self.addSubInterface(self.albumInterface,
                             'tabAlbumInterface', self.tr('Album'), ':/gallery/images/Dvd.png')
        self.addSubInterface(self.artistInterface,
                             'tabArtistInterface', self.tr('Artist'), ':/gallery/images/Singer.png')

        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        qrouter.setDefaultRouteKey(self.stackedWidget, self.baptism_interface.objectName())

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

        # 将人员信息只保留两个按钮
        self.student_widget.baseStudentFuncTemp_1.button_1.hide()
        self.student_widget.baseStudentFuncTemp_1.button_2.hide()
        self.student_widget.baseStudentFuncTemp_1.button_3.setText("将选中人员填充到上表")
        self.student_widget.baseStudentFuncTemp_1.button_3.clicked.connect(self.setDataFromStudnetWidget)
        self.student_widget.baseStudentFuncTemp_1.button_4.setText("清除选择")

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

    def setDataFromStudnetWidget(self):
        idx = self.student_widget.baseStudentFuncTemp_1.tableWidget.currentRow()
        if idx == -1:
            return

        if self.stackedWidget.currentIndex() == 0:
            student_info = self.student_widget.students[idx]
            self.baptism_interface.seteveninfoFromParent(student_info)
