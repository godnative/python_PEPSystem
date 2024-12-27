from DataBase.base_db import DataBaseManage

class UserDB(DataBaseManage):
    def user_login_check(self, username, password):
        # 定义查询语句
        query = """
                SELECT * FROM user WHERE user_name = ? AND user_password = ?
               """
        params = (username, password)
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params,single=True)

if __name__ == '__main__':
    with UserDB() as db:
        result = db.user_login_check("admin", "password1")
        print(result)
