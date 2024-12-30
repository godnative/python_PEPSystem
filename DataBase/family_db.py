# database/classes_db.py文件中
# 从数据库模块中导入基础数据库管理类 DatabaseManage
from DataBase.base_db import DataBaseManage


# 定义一个类 ClassDB，继承自 DatabaseManage
class FamilyDB(DataBaseManage):
    # 定义一个方法 fetch_classes，用于从数据库中获取班级信息
    def fetch_family(self):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
            SELECT * FROM school
            """
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)

    def add_family(self, family_info):
        query = """
                INSERT INTO family (family_name, family_address, family_school_id)
                VALUES (?, ?, ?)
            """
        params = (family_info['family_name'], family_info['family_address'], family_info['family_school_id'])
        return self.execute_query(query, params)

    def modify_family(self, family_info):
        query = """
                UPDATE family SET family_name = ?, family_address = ?, family_school_id = ?
                WHERE family_id = ?
            """
        params = (family_info['family_name'], family_info['family_address'], family_info['family_school_id'],
                  family_info['family_id'])
        return self.execute_query(query, params)

    def query_family_count(self):
        query = """
        SELECT COUNT(*) FROM family
        """
        return self.fetch_query(query)


if __name__ == '__main__':
    with FamilyDB() as db:
        family_info = {
            'family_name': '<NAME>',
            'family_address': '123 Main Street',
            'family_school_id': 1,
        }
        # db.add_family(family_info)
        print(db.query_family_count())
