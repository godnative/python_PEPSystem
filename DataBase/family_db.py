# database/classes_db.py文件中
# 从数据库模块中导入基础数据库管理类 DatabaseManage
import random

from DataBase.base_db import DataBaseManage


# 定义一个类 ClassDB，继承自 DatabaseManage
class FamilyDB(DataBaseManage):
    def __init__(self):
        super().__init__()

    # 定义一个方法 fetch_classes，用于从数据库中获取班级信息
    def fetch_family(self):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM family
        """
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)

    def add_family(self, family):
        query = """
        INSERT INTO family ( family_name, family_address, family_school_id, family_notes
        ) VALUES (?, ?, ?, ?)
        """
        params = (family["family_name"], family["family_address"], family["family_school_id"], family["family_notes"])
        return self.execute_query(query, params)

    def get_family_cnt(self):
        query = """
        SELECT COUNT(*) FROM family
        """
        return self.fetch_query(query)[0]["COUNT(*)"]


if __name__ == '__main__':
    with FamilyDB("./data.db") as db:
        for i in range(100):
            family_name = "崇义第%d号家庭" % (i + 4)
            family_address = "%d Main Street" % (random.randint(0, 1000))
            family_info = {
                "family_name": family_name,
                "family_address": family_address,
                "family_school_id": 0,
            }
            db.add_family(family_info)
        print(db.get_family_cnt())
