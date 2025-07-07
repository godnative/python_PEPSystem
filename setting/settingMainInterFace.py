# coding:utf-8
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget
from qframelesswindow import FramelessWindow, StandardTitleBar

from setting.setting_interface import SettingInterface


class SettingMainInterFace(QWidget):

    def __init__(self, ObjectName):
        super().__init__()
        self.setObjectName(ObjectName)
        self.hBoxLayout = QHBoxLayout(self)
        self.settingInterface = SettingInterface()
        self.hBoxLayout.addWidget(self.settingInterface)


if __name__ == '__main__':
    # enable dpi scale
    # create application
    app = QApplication(sys.argv)

    # create main window
    w = SettingMainInterFace()
    w.resize(800, 600)
    w.show()
    app.exec()
