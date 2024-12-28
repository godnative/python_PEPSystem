import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout


class ProfileWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Profile Information')
        self.setGeometry(100, 100, 400, 300)

        # 创建头像标签
        self.avatar_label = QLabel(self)
        pixmap = QPixmap('path_to_your_avatar_image.png')  # 替换为你的头像图片路径
        self.avatar_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 创建信息标签
        self.name_label = QLabel('姓名: 张三', self)
        self.student_id_label = QLabel('学号: 12345678', self)
        self.address_label = QLabel('家庭住址: 北京市朝阳区', self)

        # 使用QVBoxLayout来组织布局
        main_layout = QVBoxLayout()

        # 使用QHBoxLayout来组织头像和信息部分
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.avatar_label)
        header_layout.addStretch(1)  # 添加一个伸缩因子，使信息部分靠右对齐

        # 使用QGridLayout来组织信息部分
        info_layout = QGridLayout()
        info_layout.addWidget(self.name_label, 0, 0)
        info_layout.addWidget(self.student_id_label, 1, 0)
        info_layout.addWidget(self.address_label, 2, 0)

        # 将header_layout和info_layout添加到main_layout中
        frame = QFrame(self)
        frame.setLayout(info_layout)
        frame.setFrameShape(QFrame.Shape.Box)
        frame.setFrameShadow(QFrame.Shadow.Plain)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(frame)

        self.setLayout(main_layout)


class ParentProfileWidget(ProfileWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initParentUI()

    def initParentUI(self):
        # 在原有的基础上添加父母信息
        self.parent_name_label = QLabel('父亲姓名: 李四', self)
        self.parent_job_label = QLabel('父亲职业: 工程师', self)
        self.mother_name_label = QLabel('母亲姓名: 王五', self)
        self.mother_job_label = QLabel('母亲职业: 教师', self)

        # 创建一个新的 QGridLayout 来组织父母信息
        parent_info_layout = QGridLayout()
        parent_info_layout.addWidget(self.parent_name_label, 0, 0)
        parent_info_layout.addWidget(self.parent_job_label, 1, 0)
        parent_info_layout.addWidget(self.mother_name_label, 2, 0)
        parent_info_layout.addWidget(self.mother_job_label, 3, 0)

        # 获取原有的信息布局框架
        info_frame = self.layout().itemAt(1).widget()  # 假设信息部分在 main_layout 的第二个位置
        # 获取原有的信息布局
        original_info_layout = info_frame.layout()

        # 创建一个新的 QVBoxLayout 来包裹原有的信息布局和新添加的父母信息布局
        new_info_layout = QVBoxLayout()
        new_info_layout.addLayout(original_info_layout)
        new_info_layout.addLayout(parent_info_layout)

        # 将新的 QVBoxLayout 设置给信息框架
        info_frame.setLayout(new_info_layout)


# 主程序入口
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建并显示包含父母信息的 ParentProfileWidget
    parent_profile_widget = ParentProfileWidget(None)
    parent_profile_widget.show()

    sys.exit(app.exec())
