from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from qfluentwidgets import MessageBoxBase, SubtitleLabel

from BaseWidgets.BaseModule import BaseMainInterface, BaseMessageBoxWidget


class Parishioner_Add_MessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('添加人员', self)
        self.Parishioner_Info_Edit_widgets = BaseMessageBoxWidget(self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.Parishioner_Info_Edit_widgets)

        # 设置UI
        self.Parishioner_Info_Edit_widgets.label_1.setText("姓名")
        self.Parishioner_Info_Edit_widgets.label_2.setText("圣名")
        self.Parishioner_Info_Edit_widgets.label_3.setText("手机")
        self.Parishioner_Info_Edit_widgets.label_4.setText("身份证")
        self.Parishioner_Info_Edit_widgets.label_9.setText("性别")
        self.Parishioner_Info_Edit_widgets.label_10.setText("出生日期")
        self.Parishioner_Info_Edit_widgets.label_11.setText("备注")

        self.Parishioner_Info_Edit_widgets.label_5.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_5.hide()
        self.Parishioner_Info_Edit_widgets.label_6.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_6.hide()
        self.Parishioner_Info_Edit_widgets.label_7.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_7.hide()
        self.Parishioner_Info_Edit_widgets.label_8.hide()
        self.Parishioner_Info_Edit_widgets.inputLine_8.hide()

        self.Parishioner_Info_Edit_widgets.pic.setMaximumSize(100, 100)
        pixmap = QPixmap("./resource/pic/2.png").scaled(
            self.Parishioner_Info_Edit_widgets.pic.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.Parishioner_Info_Edit_widgets.pic.setPixmap(pixmap)

        self.widget.setMinimumWidth(350)

    def validate(self):
        """ 重写验证表单数据的方法 """
        return True


class Parishioner_Main_Interface(QWidget):

    def __init__(self):
        super().__init__()

        # 创建主布局
        main_layout = QVBoxLayout(self)

        self.BaseMainInterface = BaseMainInterface(self)
        self.BaseMainInterface.label.setMinimumSize(100, 100)
        # self.BaseMainInterface.label.setText("Parishioner")
        pixmap = QPixmap("./resource/pic/1.png").scaled(
            self.BaseMainInterface.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.label.setPixmap(pixmap)
        self.BaseMainInterface.label_2.setText("添加人员")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中

        self.resize(800, 600)

        self.BaseMainInterface.BaseQuery.addButton.clicked.connect(self.open_url)
        # w = CustomMessageBox(self)
        # if w.exec():
        #      print(w.titleLabel.text())

    def open_url(self):
        w = Parishioner_Add_MessageBox(self)
        if w.exec():
            print(w.titleLabel.text())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    main_window = Parishioner_Main_Interface()
    main_window.show()

    sys.exit(app.exec())
