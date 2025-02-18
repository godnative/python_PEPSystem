from datetime import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QFileDialog


def qdate_to_timestamp(date):
    # 将 QDate 转换为 datetime 对象
    date_time = datetime(date.year(), date.month(), date.day())
    # 将 datetime 对象转换为时间戳（秒）
    timestamp = (date_time - datetime(1970, 1, 1)).total_seconds()
    return int(timestamp)


# 时间戳转换为 QDate
def timestamp_to_date(timestamp):
    # 将时间戳（秒）转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)
    date = QDate(dt_object.year, dt_object.month, dt_object.day)
    return date


def get_now_date():
    now = datetime.now()
    date = QDate(now.year, now.month, now.day)
    return date


def get_datestr_from_timestamp(timestamp):
    date_time = datetime.utcfromtimestamp(timestamp)
    formatted_date = date_time.strftime("%Y-%m-%d")
    return formatted_date


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("点击此处上传图片")
        self.setStyleSheet("QLabel { border: 2px dashed #CCCCCC; }")
        self.uploaded_image = False
        self.setMinimumSize(200, 200)
        self.mousePressEvent = self.open_file_dialog

    def open_file_dialog(self, event=None):
        if self.uploaded_image is False:
            return
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                image_path = file_paths[0]
                self.setPixmap(QPixmap(image_path))
                self.image_path = image_path


if __name__ == '__main__':
    print(get_now_date())
    print(timestamp_to_date(1692492800))
