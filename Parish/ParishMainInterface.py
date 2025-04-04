import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCharts import QBarSet, QBarSeries, QChart, QChartView, QBarCategoryAxis
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem
from qfluentwidgets import CardWidget, IconWidget, InfoBarIcon, StrongBodyLabel, TransparentToolButton, FluentIcon


class FruitChartWidget(CardWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("fruitChartCard")

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
        self.dailyProgressLabel = StrongBodyLabel(text="水果数量柱状图", parent=self)
        self.horizontalLayout_title.addWidget(self.dailyProgressLabel)
        spacerItem1 = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_title.addItem(spacerItem1)
        self.editButton = TransparentToolButton(parent=self)
        self.editButton.setIcon(FluentIcon.EDIT)
        self.horizontalLayout_title.addWidget(self.editButton)
        self.verticalLayout.addLayout(self.horizontalLayout_title)

        # 初始水果数量
        self.apple_count = 20
        self.banana_count = 15
        self.orange_count = 25

        # 创建柱状图
        self.init_chart()

    def init_chart(self):
        # 创建柱状图的数据集合
        self.set0 = QBarSet("水果数量")
        self.set0.append([self.apple_count, self.banana_count, self.orange_count])

        # 创建柱状图系列
        self.series = QBarSeries()
        self.series.append(self.set0)

        # 创建柱状图
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("三种水果的数量柱状图")

        # 设置 X 轴标签
        categories = ["苹果", "香蕉", "橙子"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(axis_x)

        # 设置 Y 轴
        self.chart.createDefaultAxes()

        # 创建图表视图
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        self.verticalLayout.addWidget(self.chart_view)

    def update_fruit_counts(self, apple_count, banana_count, orange_count):
        # 清空原有的数据
        self.set0.remove(0, len(self.set0))

        # 更新水果数量
        self.apple_count = apple_count
        self.banana_count = banana_count
        self.orange_count = orange_count

        # 添加新的数据
        self.set0.append([self.apple_count, self.banana_count, self.orange_count])

        # 更新图表
        self.chart.removeAllSeries()
        self.chart.addSeries(self.series)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = FruitChartWidget()
    window.setFixedSize(800, 800)
    window.show()

    # 模拟动态修改水果数量
    window.update_fruit_counts(30, 20, 25)

    sys.exit(app.exec())
