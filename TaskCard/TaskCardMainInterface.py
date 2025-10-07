import random

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCharts import (
    QChart, QChartView, QPieSeries, QBarSet, QBarSeries, QBarCategoryAxis,
    QValueAxis
)
from PyQt6.QtCore import QDate
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QSpacerItem, QGridLayout
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QGroupBox
)
from qfluentwidgets import MessageBoxBase, CardWidget, LineEdit, InfoBarIcon, \
    IconWidget, FluentIcon, StrongBodyLabel, TransparentToolButton, BodyLabel, LargeTitleLabel, \
    ProgressRing, ScrollArea, CheckBox, CalendarPicker, PushButton, FlyoutView, Flyout

from DataBase.student_db import StudentDB
from utils.utils_tool import timestamp_to_date


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

    def __init__(self, login_info, parent=None):
        super().__init__(parent)
        self.login_info = login_info
        self.task_card_parishioner_info = None
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
        # noinspection PyUnresolvedReferences
        self.addTaskButton.clicked.connect(self.add_task)
        # noinspection PyUnresolvedReferences
        self.syncTaskButton.clicked.connect(self.showFlyout2)

        # 添加定时器
        self.timer = QTimer(self)
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.update_task_visibility)
        self.timer.start(3000)  # 5000 毫秒 = 5 秒

        self.RefreshTaskCard()

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

    def add_task_with_info(self, parishioner_info):
        cur_year = QDate.currentDate().year()
        parishioner_date = None
        date_str = None
        if parishioner_info["student_alive_state"] == 1:
            parishioner_date = QDate.fromString(parishioner_info["student_birthday"], "yyyy-mm-dd")
            date_str = "生日提醒"
        else:
            parishioner_date = QDate.fromString(parishioner_info["student_death_anniversary"], "yyyy-mm-dd")
            date_str = "忌日提醒"
        diff_year = cur_year - parishioner_date.year()
        # 计算当前年份的日期
        parishioner_birthday = parishioner_date.addYears(diff_year)
        content = f"{parishioner_info["student_name"]}:" + date_str
        objectname = "taskCard" + str(parishioner_info["student_id"])
        todo_card = TaskCard(parishioner_birthday, content, objectname, self)
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
        # noinspection PyUnresolvedReferences
        self.taskCountsChanged.emit(self.overTimeCnt, self.finishTimeCnt, self.waitTimeCnt, percentage)

    def delete_all_tasks(self):
        for i in range(self.todo_list_layout.count()):
            item = self.todo_list_layout.itemAt(i)
            task_card = item.widget()
            if isinstance(task_card, TaskCard):
                task_card.deleteLater()
        self.update_task_visibility()

    def RefreshTaskCard(self):
        with StudentDB(self) as db:
            self.delete_all_tasks()
            self.task_card_parishioner_info = db.fetch_students_with_birthday(self.login_info["parish_id"])
            if self.task_card_parishioner_info:
                for i in self.task_card_parishioner_info:
                    self.add_task_with_info(i)

    def showFlyout2(self):
        view = FlyoutView(
            title='确认同步数据',
            content="同步数据会清除已完成标记，并从当月开始从新添加所有的生日提醒",
            isClosable=False
            # image='resource/yiku.gif',
        )

        # add button to view
        button = PushButton()
        button.setText("同步")
        # noinspection PyUnresolvedReferences
        button.clicked.connect(self.RefreshTaskCard)
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        w = Flyout.make(view, self.syncTaskButton, self)
        view.closed.connect(w.close)

class ChartUpdater(QObject):
    """用于跨线程更新图表的信号类"""
    update_pie_signal = pyqtSignal(dict)
    update_bar_signal = pyqtSignal(list)

# noinspection PyUnresolvedReferences
class ParishDashboard(QWidget):
    def __init__(self, login_info):
        super().__init__()
        self.login_info = login_info
        self.cur_parish_id = self.login_info['parish_id']
        self.setWindowTitle("数据可视化仪表板")

        # 创建信号对象
        self.chart_updater = ChartUpdater()

        # 初始化UI
        self.init_ui()

        # 连接信号槽
        # noinspection PyUnresolvedReferences
        self.chart_updater.update_pie_signal.connect(self.update_pie_chart)
        self.chart_updater.update_bar_signal.connect(self.update_bar_chart)
        # 创建图表
        self.create_pie_chart()
        self.create_bar_chart()

        self.simulate_data_updates()

    def init_ui(self):
        """初始化用户界面"""

        # 左侧图表区域
        up_layout = QHBoxLayout(self)

        # 饼图组
        pie_group = QGroupBox("领洗人员数量")
        pie_layout = QVBoxLayout()
        self.pie_chart_view = QChartView()
        self.pie_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        pie_layout.addWidget(self.pie_chart_view)
        pie_group.setLayout(pie_layout)
        up_layout.addWidget(pie_group)

        # 柱状图组
        bar_group = QGroupBox("人员年龄分布")
        bar_layout = QVBoxLayout()
        self.bar_chart_view = QChartView()
        self.bar_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        bar_layout.addWidget(self.bar_chart_view)
        bar_group.setLayout(bar_layout)
        up_layout.addWidget(bar_group)

    def create_pie_chart(self):
        """创建饼图"""
        self.pie_series = QPieSeries()
        self.pie_series.setHoleSize(0.35)

        # 创建图表
        chart = QChart()
        chart.addSeries(self.pie_series)
        chart.setTitle("人员领洗比例")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        self.pie_chart_view.setChart(chart)

    def create_bar_chart(self):
        """创建柱状图"""
        self.bar_series = QBarSeries()
        self.bar_set = QBarSet("人数")

        # 统计年龄段
        parishioner_age_data = [random.randint(0, 90) for _ in range(50)]
        self.update_bar_statistics(parishioner_age_data)

        self.bar_series.append(self.bar_set)

        # 创建图表
        chart = QChart()
        chart.addSeries(self.bar_series)
        chart.setTitle("人员年龄分布")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # X轴
        self.bar_categories = ["0-20岁", "20-40岁", "40-60岁", "60岁以上"]
        axis_x = QBarCategoryAxis()
        axis_x.append(self.bar_categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.bar_series.attachAxis(axis_x)

        # Y轴
        axis_y = QValueAxis()
        axis_y.setTitleText("人数")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        self.bar_series.attachAxis(axis_y)

        self.bar_chart_view.setChart(chart)

    def update_bar_statistics(self, age_data):
        """更新柱状图统计数据"""
        # 先移除所有数据点（PyQt6中QBarSet没有clear方法，需要逐个移除）
        while self.bar_set.count() > 0:
            self.bar_set.remove(0)

        # 统计各年龄段人数
        age_groups = {
            "0-20岁": 0,
            "20-40岁": 0,
            "40-60岁": 0,
            "60岁以上": 0
        }

        for age in age_data:
            if age < 20:
                age_groups["0-20岁"] += 1
            elif 20 <= age < 40:
                age_groups["20-40岁"] += 1
            elif 40 <= age < 60:
                age_groups["40-60岁"] += 1
            else:
                age_groups["60岁以上"] += 1
        # 添加到柱状图数据集
        for count in age_groups.values():
            self.bar_set.append(count)

    def simulate_data_updates(self):
        """模拟数据更新（可以在其他线程中调用）"""

        # 更新水果数据（线程安全）
        total_student = 0
        none_holy_name_student = 0
        age_cnt = 0
        with StudentDB(self) as db:
            total_student = db.get_parishioner_cnt_with_parish_id(self.cur_parish_id)
            none_holy_name_student = db.get_parishioner_none_holy_name_cnt_with_parish_id(self.cur_parish_id)
            age_cnt = db.get_parishioner_age_with_parish_id(self.cur_parish_id)
            print(age_cnt)
        parishioner_baptism_info = {
            "领洗人数": total_student - none_holy_name_student,
            "未领洗人数": none_holy_name_student
        }
        self.chart_updater.update_pie_signal.emit(parishioner_baptism_info)

        # 更新年龄数据（添加一些新数据）
        self.chart_updater.update_bar_signal.emit(age_cnt)

    def update_pie_chart(self, new_data):
        """更新饼图（通过信号槽调用）"""
        self.pie_series.clear()

        for fruit, count in new_data.items():
            slice_ = self.pie_series.append(f"{fruit}: {count}", count)
            slice_.setLabelVisible(True)

    def update_bar_chart(self, age_data):
        """更新柱状图（通过信号槽调用）"""
        self.update_bar_statistics(age_data)

        # 获取图表并强制更新
        chart = self.bar_chart_view.chart()
        if chart:
            chart.update()  # 使用 QChart 的 update() 方法而不是 QBarSeries 的 invalidate()

class ProcessDashboard(QWidget):
    def __init__(self, login_info):
        super().__init__()
        self.login_info = login_info
        # 创建信号对象
        self.chart_updater = ChartUpdater()

        # 初始化UI
        self.init_ui()

        # 连接信号槽
        # noinspection PyUnresolvedReferences
        self.chart_updater.update_pie_signal.connect(self.update_pie_chart)
        # 创建图表
        self.create_pie_chart()

        parishioner_baptism_info = {
            "逾期": 65,
            "已完成": 38,
            "未完成": 20,
        }
        # noinspection PyUnresolvedReferences
        self.chart_updater.update_pie_signal.emit(parishioner_baptism_info)

    def init_ui(self):
        """初始化用户界面"""

        # 左侧图表区域
        up_layout = QHBoxLayout(self)
        # 饼图组
        pie_group = QGroupBox("任务完成情况")
        pie_layout = QVBoxLayout()
        self.pie_chart_view = QChartView()
        self.pie_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        pie_layout.addWidget(self.pie_chart_view)
        pie_group.setLayout(pie_layout)
        up_layout.addWidget(pie_group)

    def create_pie_chart(self):
        """创建饼图"""
        self.pie_series = QPieSeries()
        self.pie_series.setHoleSize(0.35)

        # 创建图表
        chart = QChart()
        chart.addSeries(self.pie_series)
        chart.setTitle("任务完成情况")
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)

        self.pie_chart_view.setChart(chart)

    def update_pie_chart(self, new_data):
        """更新饼图（通过信号槽调用）"""
        self.pie_series.clear()

        for fruit, count in new_data.items():
            slice_ = self.pie_series.append(f"{fruit}: {count}", count)
            slice_.setLabelVisible(True)


class TaskCardMainInterFace(QWidget):
    taskcardwaitfinishnumchanged = pyqtSignal(int)

    def __init__(self, login_info, objectname, parent=None):
        super().__init__(parent)
        self.login_info = login_info
        self.task_card_parishioner_info = None
        self.setObjectName(objectname)

        main_layout = QGridLayout(self)

        self.ParishDashboard = ParishDashboard(self.login_info)
        main_layout.addWidget(self.ParishDashboard, 0,0,1,2)

        # 实际功能界面
        self.process_card = ProcessDashboard(self.login_info)
        self.task_card_main = TaskCardMain(self.login_info, self)
        self.process_card.setMinimumHeight(500)
        main_layout.addWidget(self.process_card, 1, 0)
        main_layout.addWidget(self.task_card_main, 1, 1)



        # 连接信号量
        # noinspection PyUnresolvedReferences
        self.task_card_main.taskCountsChanged.connect(self.setOFWValue)

    def setOFWValue(self, overTime, finishTime, waitTime, percentage):
        parishioner_baptism_info = {
            "逾期": overTime,
            "已完成": finishTime,
            "未完成": waitTime,
        }
        # noinspection PyUnresolvedReferences
        self.process_card.chart_updater.update_pie_signal.emit(parishioner_baptism_info)
        # noinspection PyUnresolvedReferences
        self.taskcardwaitfinishnumchanged.emit(waitTime)
