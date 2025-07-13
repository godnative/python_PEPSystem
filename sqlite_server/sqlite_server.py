# main.py（更新后的 PyQt6 界面）
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QMessageBox, QGroupBox)
from PyQt6.QtCore import Qt
from flask_server import FlaskServer


class ServerControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flask 服务器管理")
        self.setFixedSize(500, 300)
        self.flask_server = None
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 配置组
        config_group = QGroupBox("服务器配置")
        config_layout = QVBoxLayout()

        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("监听 IP:"))
        self.ip_input = QLineEdit("127.0.0.1")
        ip_layout.addWidget(self.ip_input)
        config_layout.addLayout(ip_layout)

        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("监听端口:"))
        self.port_input = QLineEdit("5000")
        port_layout.addWidget(self.port_input)
        config_layout.addLayout(port_layout)

        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # 控制按钮
        self.toggle_button = QPushButton("启动服务器")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_server)

        self.status_label = QLabel("状态: 已停止")
        self.status_label.setStyleSheet("color: red;")

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.toggle_button)
        control_layout.addWidget(self.status_label)
        main_layout.addLayout(control_layout)
        main_layout.addStretch()

    def toggle_server(self, checked):
        if checked:
            host = self.ip_input.text().strip()
            port = self.port_input.text().strip()

            if not host or not port:
                QMessageBox.critical(self, "错误", "请填写有效的IP和端口")
                self.toggle_button.setChecked(False)
                return

            try:
                port = int(port)
                if not 0 < port < 65536:
                    raise ValueError
            except ValueError:
                QMessageBox.critical(self, "错误", "端口必须是1-65535之间的整数")
                self.toggle_button.setChecked(False)
                return

            try:
                self.flask_server = FlaskServer(host=host, port=port)
                self.flask_server.start()
                self.status_label.setText(f"状态: 运行中 (http://{host}:{port})")
                self.status_label.setStyleSheet("color: green;")
                self.toggle_button.setText("停止服务器")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法启动服务器: {str(e)}")
                self.toggle_button.setChecked(False)
        else:
            if self.flask_server:
                self.flask_server.stop()
                self.flask_server = None
            self.status_label.setText("状态: 已停止")
            self.status_label.setStyleSheet("color: red;")
            self.toggle_button.setText("启动服务器")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServerControlWindow()
    window.show()
    sys.exit(app.exec())