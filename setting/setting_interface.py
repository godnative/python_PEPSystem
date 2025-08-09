# coding:utf-8
import os
import shutil
from datetime import datetime
from typing import Union

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QPushButton
from qfluentwidgets import FluentIcon as FIF, SwitchSettingCard
from qfluentwidgets import (SettingCardGroup, PushSettingCard,
                            ScrollArea,
                            ExpandLayout, SettingCard, FluentIconBase, HyperlinkButton)

from sqlite_server.flask_server import FlaskServer
from utils.msyscfg import CUR_SYS_TYPE
if CUR_SYS_TYPE == 0:
    from utils.msyscfg import SYSTEM_DATABASE_BACKUP_FILE_PATH, SYSTEM_DATABASE_FILE_PATH, AUTHOR, VERSION
else:
    from utils.msyscfg import AUTHOR, VERSION


class PushAndLinkSettingCard(SettingCard):
    """ Setting card with a push button """

    clicked = pyqtSignal()

    def __init__(self, url, button_text, url_text, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                 parent=None):
        super().__init__(icon, title, content, parent)
        self.button = QPushButton(button_text, self)
        self.linkButton = HyperlinkButton(url, url_text, self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addWidget(self.linkButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)
        # noinspection PyUnresolvedReferences
        self.button.clicked.connect(self.clicked)


class SettingInterface(ScrollArea):
    """ Setting interface """

    downloadFolderChanged = pyqtSignal(str)
    acrylicEnableChanged = pyqtSignal(bool)

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
        if CUR_SYS_TYPE == 0:
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

            self.personalGroup = SettingCardGroup(
                self.tr('开放服务器端口'), self.scrollWidget)

            self.enableAcrylicCard = SwitchSettingCard(
                FIF.TRANSPARENT,
                self.tr("开启服务器端口"),
                self.tr("状态: 停止运行"),
                configItem=None,
                parent=self.personalGroup
            )

        # application
        self.aboutGroup = SettingCardGroup(
            self.tr('关于'), self.scrollWidget)

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

        if CUR_SYS_TYPE == 0:
            self.musicInThisPCGroup.addSettingCard(self.BackUpDataBaseCard)
            self.musicInThisPCGroup.addSettingCard(self.restoreDataBaseCard)

            self.personalGroup.addSettingCard(self.enableAcrylicCard)

        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        if CUR_SYS_TYPE == 0:
            self.expandLayout.addWidget(self.musicInThisPCGroup)
            self.expandLayout.addWidget(self.personalGroup)
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

    @staticmethod
    def __onBackUpDataBaseCardClicked():
        """ download folder card clicked slot """
        if os.path.exists(SYSTEM_DATABASE_BACKUP_FILE_PATH):
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S")
            shutil.copy(SYSTEM_DATABASE_FILE_PATH,
                        SYSTEM_DATABASE_BACKUP_FILE_PATH + '/database_' + formatted_time + '.db')
        else:
            print("file not exist")

    def __acrylicEnableChanged(self, enabled: bool):
        host = "0.0.0.0"
        port = 54321
        if enabled:
            try:
                self.flask_server = FlaskServer(host=host, port=port)
                self.flask_server.start()
                self.enableAcrylicCard.contentLabel.setText(f"状态: 运行中 (http://{host}:{port})")
            except Exception as e:
                self.enableAcrylicCard.contentLabel.setText(f"无法启动服务器: {str(e)}")
        else:
            if self.flask_server:
                self.flask_server.stop()
                self.flask_server = None
            self.enableAcrylicCard.contentLabel.setText(f"状态: 停止运行 (http://{host}:{port})")

    def __connectSignalToSlot(self):
        if CUR_SYS_TYPE == 0:
            self.restoreDataBaseCard.clicked.connect(
                self.__onRestoreDataBaseCardClicked)

            # noinspection PyUnresolvedReferences
            self.BackUpDataBaseCard.clicked.connect(
                self.__onBackUpDataBaseCardClicked
            )

            self.enableAcrylicCard.checkedChanged.connect(
                self.__acrylicEnableChanged)
