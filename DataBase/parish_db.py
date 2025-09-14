# database/classes_db.py文件中
# 从数据库模块中导入基础数据库管理类 DatabaseManage
import random

from DataBase.base_db import DataBaseManage


# 定义一个类 ClassDB，继承自 DatabaseManage
class ParishDb(DataBaseManage):
    # 定义一个方法 fetch_classes，用于从数据库中获取班级信息
    def fetch_parish(self):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM parish
        """
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)

    def add_parish(self, parish):
        query = """
            INSERT INTO parish (parish_name, 
                                parish_date, 
                                parish_address, 
                                parish_info, 
                                parish_pic_path, 
                                parish_priest,
                                parish_phonenum)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (parish['parish_name'], parish['parish_date'], parish['parish_address'],
                  parish['parish_info'], parish['parish_pic_path'], parish['parish_priest'], parish['parish_phonenum'])
        return self.execute_query(query, params)

    def get_parish_info(self, parish_id):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM parish WHERE parish_id = ?
        """
        params = (parish_id,)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        ret = self.fetch_query(query, params=params)
        if not ret:
            return None
        else:
            return ret[0]

    def get_max_parish_id(self):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT MAX(parish_id) FROM parish
        """
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)[0]

    def check_parish_name(self, parish_name):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM parish WHERE parish_name == ?
        """
        params = (parish_name,)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def modify_parish(self, parish):
        query = """
            UPDATE parish SET parish_date = ?, 
                            parish_address = ?, 
                            parish_info = ?, 
                            parish_pic_path = ?,
                            parish_priest = ?,
                            parish_phonenum = ?
            WHERE parish_name = ?
        """
        params = (parish['parish_date'], parish['parish_address'], parish['parish_info'],
                  parish['parish_pic_path'],parish['parish_priest'], parish['parish_phonenum'],
                  parish['parish_name'])
        return self.execute_query(query, params)


if __name__ == '__main__':
    with ParishDb(None) as db:
        for i in range(10):
            family_name = "崇义小学第%d号家庭" % (i + 1)
            family_address = "%d Main Street" % (random.randint(0, 1000))
            school_info = {
                "family_name": family_name,
                "family_address": family_address,
                "family_school_id": 1,
                "family_notes": "无备注"
            }
            db.add_family(school_info)
