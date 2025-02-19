import enum

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from qfluentwidgets import MessageBoxBase, SubtitleLabel, InfoBar

from BaseWidgets.BaseModule import BaseMainInterface, BaseMessageBoxWidget
from DataBase.holyevent_db import HolyEventDB
from Parishioner.Parishioner_Interface import Parishioner_Main_Interface
from utils.utils_tool import qdate_to_timestamp, timestamp_to_date


class QUERY_TYPE(enum.Enum):
    QUERY_ONE = 0
    QUERY_ALL = 1
    QUERY_LIKE = 2


class EventConfirmation_MessageBox(MessageBoxBase):

    def __init__(self, cur_parish, parent=None):
        super().__init__(parent)
        self.family_info = None
        self.cur_parish = cur_parish
        self.parishioner_widgets = Parishioner_Main_Interface(self.cur_parish, 1,
                                                              "Parishioner_Main_Interface_from_EventConfirmation_MessageBox")
        self.parishioner_1_id = None
        self.parishioner_2_id = None
        self.titleLabel = SubtitleLabel('人员', self)
        self.BaseMessageBoxWidget = BaseMessageBoxWidget(self)

        self.parishioner_widgets.BaseMainInterface.BaseQuery.extendButton_1.show()
        self.parishioner_widgets.BaseMainInterface.BaseQuery.extendButton_1.setText("添加选中人员")
        self.parishioner_widgets.BaseMainInterface.BaseQuery.delButton.hide()
        self.parishioner_widgets.BaseMainInterface.BaseQuery.ModButton.hide()
        self.parishioner_widgets.BaseMainInterface.BaseQuery.extendButton_1.clicked.connect(self.set_persion_info)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.BaseMessageBoxWidget)

        self.viewLayout.addWidget(self.parishioner_widgets)

        # 设置UI
        self.BaseMessageBoxWidget.label_1.setText("姓名")
        self.BaseMessageBoxWidget.label_2.setText("圣名")
        self.BaseMessageBoxWidget.label_3.setText("见证人")
        self.BaseMessageBoxWidget.label_4.setText("施行人")
        self.BaseMessageBoxWidget.label_9.setText("性别")
        self.BaseMessageBoxWidget.label_10.setText("日期")
        self.BaseMessageBoxWidget.label_13.setText("备注")

        self.BaseMessageBoxWidget.label_5.hide()
        self.BaseMessageBoxWidget.inputLine_5.hide()
        self.BaseMessageBoxWidget.label_6.hide()
        self.BaseMessageBoxWidget.inputLine_6.hide()
        self.BaseMessageBoxWidget.label_7.hide()
        self.BaseMessageBoxWidget.inputLine_7.hide()
        self.BaseMessageBoxWidget.label_8.hide()
        self.BaseMessageBoxWidget.inputLine_8.hide()
        self.BaseMessageBoxWidget.label_11.hide()
        self.BaseMessageBoxWidget.inputLine_11.hide()
        self.BaseMessageBoxWidget.label_12.hide()
        self.BaseMessageBoxWidget.inputLine_12.hide()

        self.parishioner_widgets.BaseMainInterface.label.hide()
        self.parishioner_widgets.BaseMainInterface.label_2.hide()

        self.BaseMessageBoxWidget.inputLine_9.addItem("男", userData=0)
        self.BaseMessageBoxWidget.inputLine_9.addItem("女", userData=1)

        self.BaseMessageBoxWidget.pic.setMaximumSize(100, 100)
        pixmap = QPixmap("./resource/pic/5.png").scaled(
            self.BaseMessageBoxWidget.pic.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMessageBoxWidget.pic.setPixmap(pixmap)

        self.widget.setMinimumWidth(350)

    def _validateInput(self):
        errors = []  # 初始化错误信息列表

        if not self.BaseMessageBoxWidget.inputLine_1.text().strip():
            errors.append("请输入姓名")  # 验证姓名是否填写，如果未填写，添加错误信息

        if not self.BaseMessageBoxWidget.inputLine_4.text().strip():
            errors.append("请输入施行人")  # 验证班级是否选择，如果未选择班级，添加错误信息

        return errors  # 返回所有错误信息

    def validate(self):
        """ 重写验证表单数据的方法 """
        errors = self._validateInput()  # 调用自定义的验证方法，返回错误信息列表
        if errors:
            error_message = "\n".join(errors)  # 如果存在错误信息，将错误信息列表转换为字符串，按行显示
            InfoBar.error(title="输入有误", content=error_message, parent=self,
                          duration=1000)  # 使用 InfoBar 显示错误提示，设置标题、内容、父窗口和持续时间
            return False
        return True  # 返回验证结果，True 表示验证通过，False 表示验证失败

    def get_InputEvenBaptismMessageinfo(self):
        evenBaptism_messageinfo = {
            'holyevent_p1_id': self.parishioner_1_id,
            'holyevent_p2_id': self.parishioner_2_id,
            'holyevent_implementer': self.BaseMessageBoxWidget.inputLine_4.text(),
            'holyevent_witness': self.BaseMessageBoxWidget.inputLine_3.text(),
            'holyevent_school_id': "",
            'holyevent_date': qdate_to_timestamp(self.BaseMessageBoxWidget.inputLine_10.date),
            'holyevent_note': self.BaseMessageBoxWidget.inputLine_13.text()
        }
        return evenBaptism_messageinfo

    def set_InputEventMessageinfo(self, evenBaptism_messageinfo):
        self.parishioner_1_id = evenBaptism_messageinfo["holyevent_p1_id"]
        self.parishioner_2_id = evenBaptism_messageinfo["holyevent_p2_id"]
        self.BaseMessageBoxWidget.inputLine_1.setText(evenBaptism_messageinfo["holyevent_p1_name"])
        self.BaseMessageBoxWidget.inputLine_2.setText(evenBaptism_messageinfo["holyevent_p1_holyname"])
        self.BaseMessageBoxWidget.inputLine_3.setText(evenBaptism_messageinfo["holyevent_witness"])
        self.BaseMessageBoxWidget.inputLine_4.setText(evenBaptism_messageinfo["holyevent_implementer"])
        self.BaseMessageBoxWidget.inputLine_9.setCurrentIndex(evenBaptism_messageinfo["holyevent_p1_gender"])
        self.BaseMessageBoxWidget.inputLine_10.setDate(timestamp_to_date(evenBaptism_messageinfo["holyevent_date"]))
        self.BaseMessageBoxWidget.inputLine_13.setText(evenBaptism_messageinfo["holyevent_note"])
        return

    def set_lineedit_uneditable(self):  # 定义一个方法，用于设置输入框不可编辑
        self.BaseMessageBoxWidget.inputLine_1.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_2.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_3.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_4.setReadOnly(True)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_9.setEnabled(False)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_10.setEnabled(False)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_11.setEnabled(False)  # 设置输入框为只读模式，禁止用户输入
        self.BaseMessageBoxWidget.inputLine_12.hide()  # 设置输入框为只读模式，禁止用户输入

    def set_persion_info(self):
        idx = self.parishioner_widgets.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            parishioner_info = self.parishioner_widgets.parishioner_info_all[idx]
            self.parishioner_1_id = parishioner_info["student_id"]
            self.BaseMessageBoxWidget.inputLine_1.setText(parishioner_info["student_name"])
            self.BaseMessageBoxWidget.inputLine_2.setText(parishioner_info["student_holyname"])
            self.BaseMessageBoxWidget.inputLine_9.setCurrentIndex(parishioner_info["student_gender"])


class EventConfirmation_Main_Interface(QWidget):
    def __init__(self, cur_parish, cur_user, ObjectName):
        super().__init__()

        # 创建主布局
        self.setObjectName(ObjectName)
        self.cur_parish = cur_parish
        self.cur_user = cur_user
        self.cur_parish_id = self.cur_parish["school_id"]
        self.Event_all_info = None

        self.evenType = 0
        main_layout = QVBoxLayout(self)

        self.BaseMainInterface = BaseMainInterface(self)
        self.BaseMainInterface.label.setMinimumSize(100, 100)
        # self.BaseMainInterface.label.setText("Parishioner")
        pixmap = QPixmap("./resource/pic/6.png").scaled(
            self.BaseMainInterface.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.BaseMainInterface.label.setPixmap(pixmap)
        self.BaseMainInterface.label_2.setText("坚振圣事")
        main_layout.addWidget(self.BaseMainInterface)  # 正确地将 ReusableWidget 作为一个整体添加到布局中


        self.BaseMainInterface.BaseQuery.addButton.clicked.connect(self.add_even)
        self.BaseMainInterface.BaseQuery.delButton.clicked.connect(self.delete_even)
        self.BaseMainInterface.BaseQuery.ModButton.clicked.connect(self.modify_even)
        self.BaseMainInterface.BaseQuery.searchInput.searchSignal.connect(self.query_evenBaptism_info_with_like)
        self.BaseMainInterface.BaseQuery.searchInput.returnPressed.connect(self.query_evenBaptism_info_with_like)

        self.evenBaptism_tableView_header = [
            "姓名", "圣名", "施行人", "见证人", "堂区", "日期", "备注"
        ]
        self.BaseMainInterface.BaseQuery.tableWidget.setColumnCount(len(self.evenBaptism_tableView_header))
        self.BaseMainInterface.BaseQuery.tableWidget.setHorizontalHeaderLabels(self.evenBaptism_tableView_header)
        self.Load_even(QUERY_TYPE.QUERY_ALL, self.evenType, self.cur_parish_id)

    def query_evenBaptism_info_with_like(self):
        if self.BaseMainInterface.BaseQuery.searchInput.text() == "":
            self.Load_even(QUERY_TYPE.QUERY_ALL, self.evenType, self.cur_parish_id)
        else:
            self.Load_even(QUERY_TYPE.QUERY_LIKE, self.evenType, self.cur_parish_id,
                           self.BaseMainInterface.BaseQuery.searchInput.text())

    def Load_even(self, query_type, even_type, school_id, query_param=None):
        with HolyEventDB() as db:
            if QUERY_TYPE.QUERY_ALL == query_type:
                self.Event_all_info = db.fetch_all_event_by_type(even_type, school_id)
            elif QUERY_TYPE.QUERY_LIKE == query_type:
                self.Event_all_info = db.fetch_even_with_like(even_type, query_param, school_id)
            else:
                return

        if self.Event_all_info is None:
            return

        header_info = [
            'holyevent_p1_name', 'holyevent_p1_holyname', 'holyevent_implementer',
            'holyevent_witness', 'holyevent_school_id', 'holyevent_date', 'holyevent_note'
        ]
        self.BaseMainInterface.BaseQuery.set_viewWidget_data(header_info, self.Event_all_info)

    def add_even(self):
        w = EventConfirmation_MessageBox(self)
        w.titleLabel.setText("添加事件")
        if w.exec():
            with HolyEventDB() as db:
                get_InputEvenBaptismMessageinfo = w.get_InputEvenBaptismMessageinfo()
                get_InputEvenBaptismMessageinfo["student_school_id"] = self.cur_parish_id
                get_InputEvenBaptismMessageinfo["holyevent_type"] = self.evenType
                db.add_even(get_InputEvenBaptismMessageinfo)
            self.Load_even(QUERY_TYPE.QUERY_ALL, self.evenType, self.cur_parish_id)

    def delete_even(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = EventConfirmation_MessageBox(self)
            w.parishioner_widgets.hide()
            w.titleLabel.setText("删除事件")
            w.set_lineedit_uneditable()
            w.set_InputEventMessageinfo(self.Event_all_info[idx])
            if w.exec():
                with HolyEventDB() as db:
                    db.delete_event(self.Event_all_info[idx]["holyevent_id"])
                    self.Load_even(QUERY_TYPE.QUERY_ALL, self.evenType, self.cur_parish_id)

    def modify_even(self):
        idx = self.BaseMainInterface.BaseQuery.tableWidget.currentRow()
        if idx != -1:
            w = EventConfirmation_MessageBox(self)
            w.parishioner_widgets.hide()
            w.titleLabel.setText("修改事件信息")
            w.set_InputEventMessageinfo(self.Event_all_info[idx])
            if w.exec():
                with HolyEventDB() as db:
                    Even_info = w.get_InputEvenBaptismMessageinfo()
                    Even_info["student_school_id"] = self.cur_parish_id
                    Even_info["holyevent_id"] = self.Event_all_info[idx]["holyevent_id"]
                    db.update_even(Even_info)
                self.Load_even(QUERY_TYPE.QUERY_ALL, self.evenType, self.cur_parish_id)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    main_window = Parishioner_Main_Interface()
    main_window.show()

    sys.exit(app.exec())
