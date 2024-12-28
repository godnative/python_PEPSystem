# database/classes_db.py文件中
# 从数据库模块中导入基础数据库管理类 DatabaseManage
from DataBase.base_db import DataBaseManage


# 定义一个类 ClassDB，继承自 DatabaseManage
class SchoolDb(DataBaseManage):
    # 定义一个方法 fetch_classes，用于从数据库中获取班级信息
    def fetch_school(self):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM school
        """
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)

    def add_school(self, school):
        query = """
            INSERT INTO school (school_name, school_date, school_address, school_info)
            VALUES (?, ?, ?, ?)
        """
        params = (school['school_name'], school['school_date'], school['school_address'], school['school_info'])
        return self.execute_query(query, params)

    def get_school_info(self, school_id):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM school WHERE school_id = ?
        """
        params = (school_id,)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, single=True, params=params)

    def check_school_name(self, school_name):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM school WHERE school_name == ?
        """
        params = (school_name,)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)


if __name__ == '__main__':
    with SchoolDb() as db:
        if db.check_school_name("柳州") is []:
            print("无")
        else:
            print("有")
