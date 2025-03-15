import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate, pyqtSignal, QTimer
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QApplication
from qfluentwidgets import MessageBoxBase, CardWidget, LineEdit, InfoBarIcon, \
    IconWidget, FluentIcon, StrongBodyLabel, TransparentToolButton, BodyLabel, LargeTitleLabel, \
    ProgressRing, ScrollArea, CheckBox, CalendarPicker, TextEdit, PushButton

from DataBase.student_db import StudentDB


class ProcessCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("progressCard")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.verticalLayout = QVBoxLayout(self)

        self.horizontalLayout_title = QHBoxLayout()
        self.horizontalLayout_title.setContentsMargins(5, -1, -1, -1)
        self.progressIcon = IconWidget(self)
        self.progressIcon.setFixedSize(24, 24)
        self.progressIcon.setIcon(InfoBarIcon.SUCCESS)
        self.horizontalLayout_title.addWidget(self.progressIcon)
        self.dailyProgressLabel = StrongBodyLabel(text="每日进度", parent=self)
        self.horizontalLayout_title.addWidget(self.dailyProgressLabel)
        spacerItem1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_title.addItem(spacerItem1)
        self.editButton = TransparentToolButton(parent=self)
        self.editButton.setIcon(FluentIcon.EDIT)
        self.horizontalLayout_title.addWidget(self.editButton)
        self.verticalLayout.addLayout(self.horizontalLayout_title)

        self.horizontalLayout_box = QHBoxLayout()

        self.verticalLayout_left_text = QVBoxLayout()
        spacerItem2 = QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_left_text.addItem(spacerItem2)
        self.overtimeLabel = BodyLabel(text="逾期", parent=self)
        self.verticalLayout_left_text.addWidget(self.overtimeLabel, 0,
                                                QtCore.Qt.AlignmentFlag.AlignHCenter |
                                                QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.overtimeNumLabel = LargeTitleLabel(text="0", parent=self)
        self.verticalLayout_left_text.addWidget(self.overtimeNumLabel, 0,
                                                QtCore.Qt.AlignmentFlag.AlignHCenter |
                                                QtCore.Qt.AlignmentFlag.AlignVCenter)
        spacerItem3 = QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_left_text.addItem(spacerItem3)

        self.verticalLayout_center_box = QVBoxLayout()
        spacerItem4 = QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_center_box.addItem(spacerItem4)

        self.progress_ring = ProgressRing(self)
        self.progress_ring.setObjectName("progressRing")
        self.progress_ring.setMaximum(100)
        self.progress_ring.setProperty("value", 0)
        self.progress_ring.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progress_ring.setTextVisible(True)
        # self.progress_ring.setUseAni(False)
        self.progress_ring.setStrokeWidth(10)
        self.progress_ring.setFormat("完成 %v%")
        self.verticalLayout_center_box.addWidget(self.progress_ring)
        spacerItem5 = QSpacerItem(20, 3, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_center_box.addItem(spacerItem5)
        self.finishTimeLabel = BodyLabel(text="已完成 :0", parent=self)
        self.verticalLayout_center_box.addWidget(self.finishTimeLabel, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem6 = QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                  QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_center_box.addItem(spacerItem6)
        self.verticalLayout_center_box.setStretch(2, 1)

        self.verticalLayout_right_text = QVBoxLayout()
        spacerItem7 = QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_right_text.addItem(spacerItem7)
        self.continousComplianceDayLabel = BodyLabel(text="待完成", parent=self)
        self.verticalLayout_right_text.addWidget(self.continousComplianceDayLabel, 0,
                                                 QtCore.Qt.AlignmentFlag.AlignHCenter |
                                                 QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.compianceDayLabel = LargeTitleLabel(text="0", parent=self)
        self.verticalLayout_right_text.addWidget(self.compianceDayLabel, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        # self.dayLabel = BodyLabel(text="天", parent=self)
        # self.verticalLayout_right_text.addWidget(self.dayLabel, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_right_text.addItem(spacerItem8)

        self.horizontalLayout_box.addLayout(self.verticalLayout_left_text)
        self.horizontalLayout_box.addLayout(self.verticalLayout_center_box)
        self.horizontalLayout_box.addLayout(self.verticalLayout_right_text)
        self.horizontalLayout_box.setStretch(0, 1)
        self.horizontalLayout_box.setStretch(1, 2)
        self.horizontalLayout_box.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_box)

    def setProgress(self, value):
        self.progress_ring.setValue(value)

    def setOFWValue(self, overTime, finishTime, waitTime, percentage):
        self.overtimeNumLabel.setText(str(overTime))
        self.finishTimeLabel.setText("已完成 :" + str(finishTime))
        self.compianceDayLabel.setText(str(waitTime))
        self.setProgress(percentage)


class TaskCard(CardWidget):
    def __init__(self, expiration_date, text, objectname, parent=None):
        super().__init__(parent)
        self.setObjectName(objectname)
        self.setMinimumSize(0, 44)
        self.setMaximumSize(600, 44)

        self.expiration_date = expiration_date
        self.completion_state = False
        self.cur_state = 0
        self.showText = text

        self.horizontalLayout_main_box = QHBoxLayout(self)
        self.horizontalLayout_main_box.setContentsMargins(15, -1, -1, -1)

        self.taskIcon1 = IconWidget(parent=self)
        self.taskIcon1.setFixedSize(QtCore.QSize(16, 16))
        self.horizontalLayout_main_box.addWidget(self.taskIcon1)

        self.taskLabel1 = BodyLabel(parent=self)
        self.taskLabel1.setProperty("pixelFontSize", 14)
        self.taskLabel1.setProperty("strikeOut", True)
        self.horizontalLayout_main_box.addWidget(self.taskLabel1)

        spacerItem19 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_main_box.addItem(spacerItem19)

        self.update_state()

    def mousePressEvent(self, event):
        self.setCompletionState()
        return super().mousePressEvent(event)

    def setCompletionState(self):
        if self.completion_state:
            self.completion_state = False
        else:
            self.completion_state = True
        self.update_state()

    def update_state(self):
        showText = self.expiration_date.toString("[yyyy-MM-dd]") + self.showText
        days_diff = QDate.currentDate().daysTo(self.expiration_date)

        # 调整计算逻辑，确保当前时间到期显示剩余 0 天
        if days_diff < 0:
            days_text = f"::超期 {-days_diff} 天"
        else:
            days_text = f"::剩余 {days_diff} 天"

        self.taskLabel1.setText(showText + days_text)

        if self.completion_state:
            self.taskIcon1.setIcon(InfoBarIcon.SUCCESS)
            self.taskLabel1.setProperty("strikeOut", True)
            self.cur_state = 0
        elif days_diff < 0:
            self.taskIcon1.setIcon(InfoBarIcon.ERROR)
            self.taskLabel1.setProperty("strikeOut", False)
            self.cur_state = 2
        else:
            self.taskIcon1.setIcon(InfoBarIcon.WARNING)
            self.taskLabel1.setProperty("strikeOut", False)
            self.cur_state = 1


class TaskCardMain(CardWidget):
    # 添加信号量
    taskCountsChanged = pyqtSignal(int, int, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumWidth(400)
        self.overTimeCnt = 0
        self.finishTimeCnt = 0
        self.waitTimeCnt = 0

        self.verticalLayout_main_vbox = QVBoxLayout(self)
        self.verticalLayout_main_vbox.setContentsMargins(8, -1, -1, -1)

        self.horizontalLayout_head_title = QHBoxLayout()
        self.taskCardIcon = IconWidget(FluentIcon.ACCEPT, parent=self)
        self.taskCardIcon.setFixedSize(18, 18)
        self.horizontalLayout_head_title.addWidget(self.taskCardIcon)
        spacerItem16 = QSpacerItem(2, 2, QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_head_title.addItem(spacerItem16)
        self.taskLabel = StrongBodyLabel(text="任务", parent=self)
        self.horizontalLayout_head_title.addWidget(self.taskLabel)
        spacerItem19 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_head_title.addItem(spacerItem19)

        self.horizontalLayout_check_box = QHBoxLayout()
        self.checkBox_1 = CheckBox(text="已完成", parent=self)
        self.checkBox_1.setChecked(True)
        self.horizontalLayout_check_box.addWidget(self.checkBox_1)
        self.checkBox_2 = CheckBox(text="未完成", parent=self)
        self.checkBox_2.setChecked(True)
        self.horizontalLayout_check_box.addWidget(self.checkBox_2)
        self.checkBox_3 = CheckBox(text="逾期", parent=self)
        self.checkBox_3.setChecked(True)
        self.horizontalLayout_check_box.addWidget(self.checkBox_3)
        self.horizontalLayout_head_title.addLayout(self.horizontalLayout_check_box)

        spacerItem17 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_head_title.addItem(spacerItem17)
        self.addTaskButton = TransparentToolButton(FluentIcon.ADD, parent=self)
        self.horizontalLayout_head_title.addWidget(self.addTaskButton)
        self.syncTaskButton = TransparentToolButton(FluentIcon.SYNC, parent=self)
        self.horizontalLayout_head_title.addWidget(self.syncTaskButton)

        self.verticalLayout_main_vbox.addLayout(self.horizontalLayout_head_title)
        spacerItem18 = QSpacerItem(20, 3, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.verticalLayout_main_vbox.addItem(spacerItem18)

        # 创建滚动区域
        self.scroll_area = ScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(300)
        # 设置 ScrollArea 的样式表以消除边框
        self.scroll_area.setStyleSheet("QScrollArea { border: none; }")

        # 创建一个包含事件列表的容器
        self.todo_container = QWidget()
        self.todo_list_layout = QVBoxLayout(self.todo_container)

        # 将容器添加到滚动区域
        self.scroll_area.setWidget(self.todo_container)

        self.verticalLayout_main_vbox.addWidget(self.scroll_area)
        self.addTaskButton.clicked.connect(self.add_task)
        self.syncTaskButton.clicked.connect(self.update_task_visibility)

        # 添加定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_task_visibility)
        self.timer.start(5000)  # 5000 毫秒 = 5 秒

    def add_task(self):
        # 创建一个新输入框和日期选择器
        input_dialog = MessageBoxBase(self)
        content_input = LineEdit(input_dialog)
        end_date_input = CalendarPicker(input_dialog)
        end_date_input.setDate(QDate.currentDate())

        input_dialog.viewLayout.addWidget(content_input)
        input_dialog.viewLayout.addWidget(end_date_input)

        if input_dialog.exec():
            content = content_input.text()
            todo_card = TaskCard(end_date_input.getDate(), content, "taskCard", self)
            self.todo_list_layout.addWidget(todo_card)

    def update_task_visibility(self):
        # 遍历 todo_list_layout 中的所有任务卡片
        self.overTimeCnt = 0
        self.finishTimeCnt = 0
        self.waitTimeCnt = 0
        for i in range(self.todo_list_layout.count()):
            item = self.todo_list_layout.itemAt(i)
            task_card = item.widget()
            if isinstance(task_card, TaskCard):
                # 根据 cur_state 判断是否隐藏或显示任务卡片
                if task_card.cur_state == 0:
                    self.finishTimeCnt += 1
                    if self.checkBox_1.isChecked():
                        task_card.show()
                    else:
                        task_card.hide()
                elif task_card.cur_state == 1:
                    self.waitTimeCnt += 1
                    if self.checkBox_2.isChecked():
                        task_card.show()
                    else:
                        task_card.hide()
                else:
                    self.overTimeCnt += 1
                    if self.checkBox_3.isChecked():
                        task_card.show()
                    else:
                        task_card.hide()

        # 计算百分比
        total = self.overTimeCnt + self.finishTimeCnt + self.waitTimeCnt
        if total > 0:
            percentage = int(self.finishTimeCnt / total * 100)
        else:
            percentage = 0

        # 发射信号
        self.taskCountsChanged.emit(self.overTimeCnt, self.finishTimeCnt, self.waitTimeCnt, percentage)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        self.printer = QPrinter()

        # 实际功能界面
        self.process_card = ProcessCard(self)
        self.process_card.setFixedSize(400, 400)
        self.task_card_main = TaskCardMain(self)
        layout.addWidget(self.process_card)
        layout.addWidget(self.task_card_main)

        name = "小明"
        self.texsss = f"""<center><font size=5>证明</font></center>\n\n***\n\n兹证明 _{name}_ 先生和 _小号_ 女士在 举 -行- 仪式"""
        name2 = "小红"

        verticalLayout = QVBoxLayout()
        self.editor = TextEdit(self)
        verticalLayout.addWidget(self.editor)
        self.editor.setMarkdown(self.texsss)
        self.pushbutton = PushButton("打印", self)
        verticalLayout.addWidget(self.pushbutton)
        self.pushbutton.clicked.connect(self.printPreview)
        layout.addLayout(verticalLayout)

        # 连接信号量
        self.task_card_main.taskCountsChanged.connect(self.process_card.setOFWValue)

    def showPrintDiaglog(self):
        printDialog = QPrintPreviewDialog(self)
        printDialog.paintRequested.connect(self.printPreview)
        # 设置打印预览对话框的标题
        printDialog.setWindowTitle("打印预览")

        if printDialog.exec():
            pass

    def showPrintDialog_2(self):
        printdialog = QPrintDialog(self)
        print("d")
        if printdialog.exec():
            self.editor.print()
            pass
            # self.editor.print(self.printer)

    def printPreview(self):
        self.editor = TextEdit()
        self.editor.setMarkdown(self.texsss)
        # self.editor.print(printer)
        printdiaglog = QPrintDialog(self.printer, self)
        if printdiaglog.exec():
            self.editor.print(self.printer)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec())
