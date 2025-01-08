# database/classes_db.py文件中
# 从数据库模块中导入基础数据库管理类 DatabaseManage

from DataBase.base_db import DataBaseManage


# 定义一个类 ClassDB，继承自 DatabaseManage
class HolyEventDB(DataBaseManage):
    def __init__(self):
        super().__init__()

    def fetch_all_event_by_type(self, event_type):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
        SELECT * FROM holyevent where holyevent_type =?
        """
        params = (event_type,)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def add_even(self, event_info):
        query = """
        INSERT INTO holyevent ( holyevent_type, holyevent_date, holyevent_witness, 
        holyevent_implementer, holyevent_p1_id, holyevent_p1_name, holyevent_p1_holyname, 
        holyevent_p2_id, holyevent_p2_name, holyevent_p2_holyname, holyevent_note, holyevent_school_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (event_info["holyevent_type"], event_info["holyevent_date"], event_info["holyevent_witness"],
                  event_info["holyevent_implementer"], event_info["holyevent_p1_id"], event_info["holyevent_p1_name"],
                  event_info["holyevent_p1_holyname"], event_info["holyevent_p2_id"], event_info["holyevent_p2_name"],
                  event_info["holyevent_p2_holyname"], event_info["holyevent_note"], event_info["holyevent_school_id"])
        return self.execute_query(query, params)

    def fetch_even_with_like(self, even_type, like_str):
        query = """
                SELECT * FROM holyevent WHERE holyevent_type = ? 
                and (holyevent_p1_name LIKE ? or holyevent_witness LIKE ? or holyevent_implementer LIKE ?)
                """
        params = (even_type, f"%{like_str}%", f"%{like_str}%", f"%{like_str}%")
        return self.fetch_query(query, params=params)


if __name__ == '__main__':
    with HolyEventDB() as db:
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
        print(db.fetch_family_with_like("527"))
