# coding:utf-8
import os
import shutil

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, RangeSettingCard, PushSettingCard,
                            ColorSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, InfoBar, CustomColorSettingCard,
                            setTheme, setThemeColor, isDarkTheme, SettingCard, FluentIconBase, HyperlinkButton)
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QStandardPaths
from PyQt6.QtGui import QDesktopServices, QFont
from PyQt6.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog, QPushButton

from typing import Union
from PyQt6.QtGui import QColor, QIcon, QPainter

from utils.msyscfg import SYSTEM_DATABASE_BACKUP_FILE_PATH, SYSTEM_DATABASE_FILE_PATH, AUTHOR, VERSION
from datetime import datetime

class PushAndLinkSettingCard(SettingCard):
    """ Setting card with a push button """

    clicked = pyqtSignal()

    def __init__(self, url, button_text, url_text, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.button = QPushButton(button_text, self)
        self.linkButton = HyperlinkButton(url, url_text, self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)
        print(self.linkButton.getUrl())

class SettingInterface(ScrollArea):
    """ Setting interface """

    downloadFolderChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("设置"), self)
        # 设置字体大小
        font = QFont()
        font.setPointSize(26)  # 设置字体大小为 16 磅
        self.settingLabel.setFont(font)

        # music folders
        self.musicInThisPCGroup = SettingCardGroup(
            self.tr("备份与恢复"), self.scrollWidget)

        self.BackUpDataBaseCard = PushAndLinkSettingCard(
            SYSTEM_DATABASE_BACKUP_FILE_PATH,
            self.tr('备份当前数据库文件'),
            self.tr('打开备份文件夹'),
            FIF.DOWNLOAD,
            self.tr("备份"),
            SYSTEM_DATABASE_BACKUP_FILE_PATH,
            self.musicInThisPCGroup
        )

        self.restoreDataBaseCard = PushSettingCard(
            self.tr('选择需要恢复的文件'),
            FIF.UPDATE,
            self.tr("恢复"),
            SYSTEM_DATABASE_BACKUP_FILE_PATH,
            self.musicInThisPCGroup
        )

        # application
        self.aboutGroup = SettingCardGroup(self.tr('关于'), self.scrollWidget)
        self.aboutCard = SettingCard(
            FIF.INFO,
            self.tr('关于'),
            '© ' + self.tr('Copyright    ') + AUTHOR +
            self.tr('    Version:') + VERSION,
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(60, 63)

        self.musicInThisPCGroup.addSettingCard(self.BackUpDataBaseCard)
        self.musicInThisPCGroup.addSettingCard(self.restoreDataBaseCard)

        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.musicInThisPCGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __onRestoreDataBaseCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getOpenFileName(
            self, self.tr("选择需要恢复的文件"), SYSTEM_DATABASE_BACKUP_FILE_PATH, filter="*.db")
        filename = folder[0]
        if filename:
            if os.path.exists(SYSTEM_DATABASE_FILE_PATH):
                shutil.copy(SYSTEM_DATABASE_FILE_PATH,
                            SYSTEM_DATABASE_FILE_PATH + 'bak')
            shutil.copy(filename,
                        SYSTEM_DATABASE_FILE_PATH)
            if os.path.exists(SYSTEM_DATABASE_FILE_PATH + 'bak'):
                os.remove(SYSTEM_DATABASE_FILE_PATH + 'bak')
            pass

    def __onBackUpDataBaseCardClicked(self):
        """ download folder card clicked slot """
        if os.path.exists(SYSTEM_DATABASE_BACKUP_FILE_PATH):
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S")
            shutil.copy(SYSTEM_DATABASE_FILE_PATH,
                        SYSTEM_DATABASE_BACKUP_FILE_PATH + '/database_'+ formatted_time + '.db')
        else:
            print("file not exist")

    def __connectSignalToSlot(self):
        self.restoreDataBaseCard.clicked.connect(
            self.__onRestoreDataBaseCardClicked)

        self.BackUpDataBaseCard.clicked.connect(
            self.__onBackUpDataBaseCardClicked
        )
