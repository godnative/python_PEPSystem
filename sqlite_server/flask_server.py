import sqlite3
import json
from flask import Flask, request, jsonify, make_response
from functools import wraps
import hashlib
import secrets
from threading import Thread
import atexit
from werkzeug.serving import make_server

from DataBase.base_db import DataBaseManage


class FlaskServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.server = None
        self.server_thread = None
        self.is_running = False

        # 配置
        self.DATABASE = 'secure_database.db'
        self.SECRET_KEY = secrets.token_hex(32)
        self.VALID_CLIENTS = {
            'client1': '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e',  # sha256 of 'password1'
            'client2': '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'  # sha256 of 'password2'
        }

        # 注册路由
        self._register_routes()

        # 确保程序退出时停止服务器
        atexit.register(self.stop)

    def _register_routes(self):
        # 装饰器：验证客户端
        def authenticate(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                auth = request.authorization
                if not auth or auth.username not in self.VALID_CLIENTS:
                    return make_response(jsonify({'error': 'Unauthorized client'}), 401)

                # provided_password_hash = hashlib.sha256(auth.password.encode()).hexdigest()
                provided_password_hash = auth.password
                if self.VALID_CLIENTS.get(auth.username) != provided_password_hash:
                    return make_response(jsonify({'error': 'Invalid credentials'}), 401)

                return f(*args, **kwargs)

            return decorated

        # 工具函数
        def get_db_connection():
            conn = sqlite3.connect(self.DATABASE)
            conn.row_factory = sqlite3.Row
            return conn

        def get_sql_type(sql):
            sql = sql.strip().lower()
            if sql.startswith('select'):
                return 'fetch'
            elif sql.startswith('insert'):
                return 'execute'
            elif sql.startswith('update'):
                return 'execute'
            elif sql.startswith('delete'):
                return 'execute'
            else:
                return 'other'

        # API端点
        @self.app.route('/execute', methods=['POST'])
        @authenticate
        def execute_sql():
            data = request.get_json()

            if 'test' in data:
                return jsonify({'result': 'success'}), 200

            if not data or 'sql' not in data:
                return jsonify({'error': 'No SQL query provided'}), 400

            sql = data['sql']
            params = data.get('params', None)

            sql_type = get_sql_type(sql)
            if sql_type == 'other':
                return jsonify({'error': 'Only SELECT, INSERT, UPDATE, DELETE statements are allowed'}), 400

            try:
                with DataBaseManage(None) as db:
                    if sql_type == 'fetch':
                        result = db.fetch_query(sql, params)
                        js_ret = {'type': 'select', 'result': result, 'count': len(result)}
                    elif sql_type == 'execute':
                        db.execute_query(sql, params)
                        js_ret = {'type': 'select', 'result': 'success', 'count': 0}
                    else:
                        js_ret = {'type': 'select', 'result': 'error', 'count': 0}
                return jsonify(js_ret)
            except Exception as e:
                return jsonify({'error': str(e)}), 400

        # 初始化数据库

    def _run(self):
        """内部方法：在单独线程中运行Flask服务器"""
        self.server = make_server(self.host, self.port, self.app)
        self.server.serve_forever()

    def start(self):
        """启动Flask服务器"""
        if not self.is_running:
            self.server_thread = Thread(target=self._run, daemon=True)
            self.server_thread.start()
            self.is_running = True
            return True
        return False

    def stop(self):
        """停止Flask服务器"""
        if self.server:
            self.server.shutdown()  # 优雅地关闭服务器
            self.server = None
            self.is_running = False
            return True
        return False