import hashlib
import sys
import json
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox,
    QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt
from requests import auth


class SQLClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flask SQL 客户端")
        self.setFixedSize(600, 500)

        self.server_url = "http://127.0.0.1:5000"  # 默认服务器地址
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ========== 服务器配置组 ==========
        config_group = QGroupBox("服务器配置")
        config_layout = QFormLayout()

        self.server_input = QLineEdit("http://127.0.0.1:54321")
        config_layout.addRow("服务器地址:", self.server_input)

        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)

        # ========== 认证信息组 ==========
        auth_group = QGroupBox("认证信息")
        auth_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setText("client1")
        self.password_input = QLineEdit()
        self.password_input.setText("password1")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        auth_layout.addRow("用户名:", self.username_input)
        auth_layout.addRow("密码:", self.password_input)

        auth_group.setLayout(auth_layout)
        main_layout.addWidget(auth_group)

        # ========== SQL 查询组 ==========
        sql_group = QGroupBox("SQL 查询")
        sql_layout = QVBoxLayout()

        self.sql_input = QTextEdit()
        self.sql_input.setPlaceholderText("输入 SQL 语句（如 SELECT * FROM users）")
        sql_layout.addWidget(self.sql_input)

        self.params_input = QTextEdit()
        self.params_input.setPlaceholderText('输入参数（JSON 格式，如 {"id": 1}，可选）')
        sql_layout.addWidget(self.params_input)

        sql_group.setLayout(sql_layout)
        main_layout.addWidget(sql_group)

        # ========== 控制按钮 ==========
        self.execute_button = QPushButton("执行查询")
        self.execute_button.clicked.connect(self.execute_query)
        main_layout.addWidget(self.execute_button)

        # ========== 结果显示组 ==========
        result_group = QGroupBox("执行结果")
        result_layout = QVBoxLayout()

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        result_layout.addWidget(self.result_output)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

    def test_server_is_online(self, server_url, username, provided_password_hash):
        # 构造请求数据
        data = {"test": 0}
        isOnline = False
        try:
            # 发送 POST 请求（带 Basic Auth）
            response = requests.post(
                f"{server_url}/execute",
                json=data,
                auth=(username, provided_password_hash),
                timeout=5
            )

            # 处理响应
            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.result_output.setPlainText(f"服务器返回错误: {result['error']}")
                else:
                    # 格式化输出结果
                    formatted_result = json.dumps(result, indent=2, ensure_ascii=False)
                    self.result_output.setPlainText(f"执行成功:\n{formatted_result}")
                    isOnline = True
            else:
                # 处理 HTTP 错误
                error_msg = f"HTTP 错误: {response.status_code}\n{response.text}"
                self.result_output.setPlainText(error_msg)

        except requests.exceptions.RequestException as e:
            # 处理连接错误
            self.result_output.setPlainText(f"连接服务器失败: {str(e)}")
        return isOnline

    def execute_query(self):
        # 获取输入数据
        server_url = self.server_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        provided_password_hash = hashlib.sha256(password.encode()).hexdigest()
        sql = self.sql_input.toPlainText().strip()
        params_text = self.params_input.toPlainText().strip()

        # 验证输入
        if not server_url or not username or not password or not sql:
            QMessageBox.warning(self, "输入错误", "请填写服务器地址、用户名、密码和 SQL 语句！")
            return

        if self.test_server_is_online(server_url, username, provided_password_hash) is False:
            QMessageBox.warning(self, "远程链接错误", "远程主机不在线")
            return

        # 解析参数（可选）
        params = None
        if params_text:
            try:
                params = json.loads(params_text)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "参数错误", "参数必须是有效的 JSON 格式！")
                return



        # 构造请求数据
        data = {"sql": sql}
        if params:
            data["params"] = params

        try:
            # 发送 POST 请求（带 Basic Auth）
            response = requests.post(
                f"{server_url}/execute",
                json=data,
                auth=(username, provided_password_hash),
                timeout=5
            )

            # 处理响应
            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.result_output.setPlainText(f"服务器返回错误: {result['error']}")
                else:
                    # 格式化输出结果
                    formatted_result = json.dumps(result, indent=2, ensure_ascii=False)
                    self.result_output.setPlainText(f"执行成功:\n{formatted_result}")
            else:
                # 处理 HTTP 错误
                error_msg = f"HTTP 错误: {response.status_code}\n{response.text}"
                self.result_output.setPlainText(error_msg)

        except requests.exceptions.RequestException as e:
            # 处理连接错误
            self.result_output.setPlainText(f"连接服务器失败: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SQLClientWindow()
    window.show()
    sys.exit(app.exec())