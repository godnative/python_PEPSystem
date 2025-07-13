# database/classes_db.py文件中
# 从数据库模块中导入基础数据库管理类 DatabaseManage

from DataBase.base_db import DataBaseManage


# 定义一个类 ClassDB，继承自 DatabaseManage
class FamilyDB(DataBaseManage):
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
        INSERT INTO family ( 
        family_name, family_address, family_school_id, 
        family_notes, operator, opera_time, opera_type
        ) VALUES (?, ?, ?, ?, ? ,?, ?)
        """
        params = (family["family_name"], family["family_address"],
                  family["family_school_id"], family["family_notes"],
                  family["operator"], family["opera_time"], family["opera_type"])
        return self.execute_query(query, params)

    def get_family_cnt_with_parish_id(self, family_school_id):
        query = """
        SELECT COUNT(*) FROM family where family_school_id = ?
        """
        params = (family_school_id,)
        return self.fetch_query(query, params=params)[0]["COUNT(*)"]

    def fetch_family_with_school_id(self, school_id):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM family where family_school_id = ?
        """
        params = (school_id,)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def fetch_family_with_family_id(self, family_id):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM family where family_id = ?
        """
        params = (family_id,)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def fetch_family_with_like(self, school_id, like_str):
        query = """
                SELECT * FROM family WHERE family_school_id = ? and ( family_name LIKE ? or family_address LIKE ? )
                """
        params = (school_id, f"%{like_str}%", f"%{like_str}%")
        return self.fetch_query(query, params=params)

    def update_family(self, family):
        query = """
                UPDATE family
                SET family_name    = ?,
                    family_address  = ?,
                    family_school_id  = ?,
                    family_notes = ?,
                    operator =?,
                    opera_time =?
                WHERE family_id = ?;
        """
        params = (family["family_name"], family["family_address"], family["family_school_id"], family["family_notes"],
                  family["operator"], family["opera_time"], family["family_id"])
        return self.execute_query(query, params)

    def delete_family(self, family_id):
        query = """
                DELETE
                FROM family
                WHERE family_id = ?;
        """
        params = (family_id,)
        return self.execute_query(query, params)

    def set_data_opera_type(self, family_id, opera_type):
        query = """
                UPDATE family
                SET opera_type = ?
                where family_id = ?;
        """
        params = (opera_type, family_id)
        return self.execute_query(query, params)


if __name__ == '__main__':
    with FamilyDB(None) as db:
        # for i in range(100):
        #     family_name = "崇义小学第%d号家庭" % (i + 1)
        #     family_address = "%d Main Street" % (random.randint(0, 1000))
        #     family_info = {
        #         "family_name": family_name,
        #         "family_address": family_address,
        #         "family_school_id": 1,
        #         "family_notes": "无备注"
        #     }
        #     db.add_family(family_info)
        print(db.get_family_cnt(0))
