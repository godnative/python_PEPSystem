# database/classes_db.py文件中
# 从数据库模块中导入基础数据库管理类 DatabaseManage

from DataBase.base_db import DataBaseManage


# 定义一个类 ClassDB，继承自 DatabaseManage
class HolyEventDB(DataBaseManage):
    def __init__(self):
        super().__init__()

    def fetch_all_event_by_type(self, event_type, school_id):
        # 定义 SQL 查询语句，用于选择 CLASSES 表中的所有数据
        query = """
            SELECT h.*,              -- 查询 student 表中的所有字段
                   s1.student_name AS holyevent_p1_name,
                   s1.student_holyname AS holyevent_p1_holyname,
                   s1.student_gender AS holyevent_p1_gender,
                   s1.student_id     AS holyevent_p1_id,
                   s2.student_name AS holyevent_p2_name,
                   s2.student_holyname AS holyevent_p2_holyname,
                   s2.student_gender AS holyevent_p2_gender,
                   s2.student_id     AS holyevent_p2_id
            -- 查询 classes 表中的 class_name 字段（班级名称）
            FROM holyevent h           -- 从 student 表中查询数据，给表取别名为 s
            JOIN student s1 ON h.holyevent_p1_id = s1.student_id
            JOIN student s2 ON h.holyevent_p2_id = s2.student_id
            where h.holyevent_type = ? and h.holyevent_school_id =?;
        """
        params = (event_type, school_id)
        # 使用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def add_even(self, event_info):
        query = """
        INSERT INTO holyevent ( holyevent_type, holyevent_date, holyevent_witness, 
        holyevent_implementer, holyevent_p1_id, holyevent_p2_id, 
        holyevent_note, holyevent_school_id,
        operator, opera_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (event_info["holyevent_type"], event_info["holyevent_date"], event_info["holyevent_witness"],
                  event_info["holyevent_implementer"], event_info["holyevent_p1_id"], event_info["holyevent_p2_id"],
                  event_info["holyevent_note"], event_info["holyevent_school_id"],
                  event_info["operator"], event_info["opera_time"])
        return self.execute_query(query, params)

    def fetch_even_with_like(self, even_type, like_str, school_id):
        query = """
                SELECT h.*,              -- 查询 student 表中的所有字段
                       s1.student_name AS holyevent_p1_name,
                       s1.student_holyname AS holyevent_p1_holyname,
                       s1.student_gender AS holyevent_p1_gender,
                       s1.student_id     AS holyevent_p1_id,
                       s2.student_name AS holyevent_p2_name,
                       s2.student_holyname AS holyevent_p2_holyname,
                       s2.student_gender AS holyevent_p2_gender,
                       s2.student_id     AS holyevent_p2_id
                -- 查询 classes 表中的 class_name 字段（班级名称）
                FROM holyevent h           -- 从 student 表中查询数据，给表取别名为 s
                JOIN student s1 ON h.holyevent_p1_id = s1.student_id
                JOIN student s2 ON h.holyevent_p2_id = s2.student_id
                where h.holyevent_type = ? and h.holyevent_school_id =?
                and (holyevent_witness LIKE ? or holyevent_implementer LIKE ?)
                """
        params = (even_type, school_id, f"%{like_str}%", f"%{like_str}%")
        return self.fetch_query(query, params=params)

    def delete_event(self, event_id):
        query = """
                DELETE
                FROM holyevent
                WHERE holyevent_id = ?;
        """
        params = (event_id,)
        return self.execute_query(query, params)

    def update_even(self, event_info):
        query = """
        UPDATE holyevent
        set holyevent_date = ?, 
            holyevent_witness = ?, 
            holyevent_implementer = ?, 
            holyevent_p1_id  = ?, 
            holyevent_p2_id = ?, 
            holyevent_note = ?, 
            holyevent_school_id = ?,
            operator =?,
            opera_time =?
        WHERE holyevent_id = ?;
        """
        params = (event_info["holyevent_date"], event_info["holyevent_witness"],
                  event_info["holyevent_implementer"], event_info["holyevent_p1_id"], event_info["holyevent_p2_id"],
                  event_info["holyevent_note"], event_info["holyevent_school_id"], event_info["holyevent_id"],
                  event_info["operator"], event_info["opera_time"])
        return self.execute_query(query, params)

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
        print(db.fetch_all_event_by_type(0))
