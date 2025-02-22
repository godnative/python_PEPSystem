from DataBase.base_db import DataBaseManage


# 定义一个名为 UserDB 的类，继承自 DataBaseManage 类，用于管理用户相关的数据库操作
class UserDB(DataBaseManage):
    def user_login_check(self, username, password):
        """
        检查用户登录信息是否正确
        :param username: 用户名
        :param password: 用户密码
        :return: 查询结果，若存在匹配记录则返回该记录，否则返回 None
        """
        # 定义查询语句，从 user 表中查找用户名和密码匹配的记录
        query = """
                SELECT * FROM user WHERE user_name = ? AND user_password = ?
               """
        # 准备查询参数
        params = (username, password)
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果，single=True 表示只取一条记录
        return self.fetch_query(query, params=params, single=True)

    def fetch_all_users(self):
        """
        从 user 表中获取所有用户的信息
        :return: 查询结果，包含所有用户的信息
        """
        # 定义查询语句，从 user 表中获取所有记录
        query = """
                SELECT * FROM user;
                """
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)

    def fetch_user_with_likestr(self, like_str):
        """
        根据模糊匹配字符串从 user 表中获取用户信息
        :param like_str: 模糊匹配的字符串
        :return: 查询结果，包含匹配的用户信息
        """
        # 定义查询语句，从 user 表中获取匹配的用户信息
        query = """
                SELECT * FROM user WHERE user_name LIKE ? OR user_note LIKE ?
                """
        # 准备查询参数，使用 % 通配符将模糊匹配字符串前后包裹起来
        params = (f"%{like_str}%", f"%{like_str}%")
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def add_user(self, user_info):
        """
        向 user 表中添加新用户
        :param user_info: 包含用户信息的字典，键为字段名，值为对应的值
        :return: 执行插入操作的结果
        """
        # 定义插入语句，将用户信息插入到 user 表的相应字段中
        query = """
                INSERT INTO user (
                user_name, user_password, user_type, user_authnum, user_note)
                VALUES (?, ?, ?, ?, ?)
                """
        # 从 user_info 字典中提取各字段的值作为查询参数
        params = (user_info["user_name"],
                  user_info["user_password"],
                  user_info["user_type"],
                  user_info["user_authnum"],
                  user_info["user_note"]
                  )
        # 调用父类的 execute_query 方法执行插入操作
        return self.execute_query(query, params=params)

    def fetch_userauthnum_with_user_id(self, user_id):
        """
        根据用户 ID 获取用户的权限编号
        :param user_id: 用户的唯一标识
        :return: 查询结果，若存在匹配记录则返回该用户的权限编号，否则返回 None
        """
        # 定义查询语句，从 user 表中查找指定用户 ID 的权限编号
        query = """
                SELECT user_authnum FROM user WHERE user_id =?
                """
        # 准备查询参数
        params = (user_id,)
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果，single=True 表示只取一条记录
        return self.fetch_query(query, params=params, single=True)

    def delete_user(self, user_id):
        """
        根据用户 ID 删除 user 表中的用户记录
        :param user_id: 用户的唯一标识
        :return: 执行删除操作的结果
        """
        # 定义删除语句，从 user 表中删除指定用户 ID 的记录
        query = """
                DELETE
                FROM user
                WHERE user_id =?;
        """
        # 准备查询参数
        params = (user_id,)
        # 调用父类的 execute_query 方法执行删除操作
        return self.execute_query(query, params=params)

    def update_user(self, user):
        """
        根据用户 ID 更新 user 表中的用户信息
        :param user: 包含用户信息的字典，键为字段名，值为对应的值，必须包含 user_id
        :return: 执行更新操作的结果
        """
        # 定义更新语句，更新 user 表中指定用户 ID 的各字段信息
        query = """
                UPDATE user
                SET user_name    =?,
                    user_password  =?,
                    user_type  =?,
                    user_authnum =?,
                    user_note =?
                WHERE user_id =?;       
        """
        # 从 user 字典中提取各字段的值作为查询参数
        params = (user["user_name"],
                  user["user_password"],
                  user["user_type"],
                  user["user_authnum"],
                  user["user_note"],
                  user["user_id"])
        # 调用父类的 execute_query 方法执行更新操作
        return self.execute_query(query, params=params)

    def update_user_password(self, user_info):
        """
        根据用户 ID 更新用户的密码
        :param user_info: 包含用户信息的字典，必须包含 user_id 和 user_password
        :return: 执行更新操作的结果
        """
        # 定义更新语句，更新 user 表中指定用户 ID 的密码
        query = """
                UPDATE user
                SET user_password  =?
                WHERE user_id =?;
        """
        # 从 user_info 字典中提取密码和用户 ID 作为查询参数
        params = (user_info["user_password"], user_info["user_id"])
        # 调用父类的 execute_query 方法执行更新操作
        return self.execute_query(query, params=params)

    def add_user_log(self, user_log_info):
        """
        向 user_log 表中添加用户日志记录
        :param user_log_info: 包含用户日志信息的字典，必须包含 user_id 和 user_log_info
        :return: 执行插入操作的结果
        """
        # 定义插入语句，将用户日志信息插入到 user_log 表中
        query = """
                INSERT INTO user_log (
                user_id, user_log_info)
                VALUES (?,?)
                """
        # 从 user_log_info 字典中提取用户 ID 和日志信息作为查询参数
        params = (user_log_info["user_id"],
                  user_log_info["user_log_info"]
                  )
        # 调用父类的 execute_query 方法执行插入操作
        return self.execute_query(query, params=params)

    def fetch_user_log(self, user_id, limit=None):
        """
        根据用户 ID 获取用户的日志记录。
        如果提供了 limit 参数，则返回指定数量的记录；否则返回所有记录。
        :param user_id: 用户的唯一标识
        :param limit: 获取日志记录的最大数量，如果为 None 则返回所有记录
        :return: 查询结果
        """
        base_query = """
                SELECT ul.*,
                       u.user_name,
                       u.user_type
                 FROM user_log ul
                 JOIN user u
                 ON ul.user_id = u.user_id
                 WHERE ul.user_id = ?
        """
        if limit is not None:
            query = base_query + " LIMIT ?"
            params = (user_id, limit)
        else:
            query = base_query
            params = (user_id,)

        return self.fetch_query(query, params=params)

    def check_user_name_exists(self, user_name):
        """
        检查数据库中是否存在指定的用户名
        :param user_name: 要检查的用户名
        :return: 如果存在返回 True，不存在返回 False
        """
        query = "SELECT * FROM user WHERE user_name = ? LIMIT 1"
        print(user_name)
        params = (user_name,)
        result = self.fetch_query(query, params=params)
        print(result)
        return result != []

if __name__ == '__main__':
    # 使用上下文管理器创建 UserDB 类的实例
    with UserDB() as db:
        # 调用 user_login_check 方法检查用户登录信息
        result = db.user_login_check("admin", "password1")
        # 打印查询结果
        print(result)