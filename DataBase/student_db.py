import random

from DataBase.base_db import DataBaseManage
from utils.name_rand import generate_chinese_name


class StudentDB(DataBaseManage):
    def fetch_students(self):
        # 定义查询语句
        query = """
               -- 查询学生表（student）中的所有字段，并关联班级表（classes），获取学生所属班级的名称
                SELECT s.*,              -- 查询 student 表中的所有字段
                       c.family_name      -- 查询 classes 表中的 class_name 字段（班级名称）
                FROM student s           -- 从 student 表中查询数据，给表取别名为 s
                JOIN family c           -- 使用 INNER JOIN 连接 classes 表，给表取别名为 c
                ON s.student_family_id = c.family_id; -- 通过 student 表的 class_id 字段与 classes 表的 class_id 字段进行匹配
               """
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)

    def add_student(self, student):
        query = """
            INSERT INTO student (student_name, student_gender, student_phonenum, student_holyname, 
                                    student_family_id, student_school_id, student_identity_num,
                                    student_birthday, student_note, operator, opera_time, opera_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (student["student_name"], student["student_gender"], student["student_phonenum"],
                  student["student_holyname"], student["student_family_id"], student["student_school_id"],
                  student["student_identity_num"], student["student_birthday"], student["student_note"],
                  student["operator"], student["opera_time"], student["opera_type"])
        return self.execute_query_return_id(query, params)

    def fetch_students_with_school_id(self, school_id):
        # 定义查询语句
        query = """
               -- 查询学生表（student）中的所有字段，并关联班级表（classes），获取学生所属班级的名称
                SELECT s.*,             -- 查询 student 表中的所有字段
                       c.family_name      -- 查询 classes 表中的 class_name 字段（班级名称）
                FROM student s           -- 从 student 表中查询数据，给表取别名为 s
                
                JOIN family c
                ON s.student_family_id = c.family_id
                where s.student_school_id = ?
               """
        params = (school_id,)
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def fetch_students_with_school_id_and_family_id(self, family_id):
        # 定义查询语句
        query = """
               -- 查询学生表（student）中的所有字段，并关联班级表（classes），获取学生所属班级的名称
                SELECT s.* ,             -- 查询 student 表中的所有字段
                        c.family_name
                FROM student s           -- 从 student 表中查询数据，给表取别名为 s
                JOIN family c
                ON s.student_family_id = c.family_id
                where s.student_family_id = ? -- 通过 student 表的 class_id 字段与 classes 表的 class_id 字段进行匹配
               """
        params = (family_id,)
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query, params=params)

    def fetch_students_with_like(self, school_id, like_str):
        query = """
                SELECT s.* ,             -- 查询 student 表中的所有字段
                        c.family_name
                FROM student s
                JOIN family c
                ON s.student_family_id = c.family_id
                WHERE student_school_id = ? and ( student_name LIKE ? or student_phonenum LIKE ? )
                """
        params = (school_id, f"%{like_str}%", f"%{like_str}%")
        return self.fetch_query(query, params=params)

    def update_student(self, student):
        query = """
                UPDATE student
                SET student_gender    = ?,
                    student_phonenum  = ?,
                    student_holyname  = ?,
                    student_family_id = ?,
                    student_school_id = ?,
                    student_name      = ?,
                    student_identity_num =?,
                    student_birthday  =?,
                    student_note      =?,
                    operator  =?,
                    opera_time=?
                WHERE student_id = ?;
        """
        params = (student["student_gender"], student["student_phonenum"], student["student_holyname"],
                  student["student_family_id"], student["student_school_id"], student["student_name"],
                  student["student_identity_num"], student["student_birthday"], student["student_note"],
                  student["operator"], student["opera_time"], student["student_id"])
        return self.execute_query(query, params)

    def delete_student(self, student_id):
        query = """
                DELETE
                FROM student
                WHERE student_id = ?;
        """
        params = (student_id,)
        return self.execute_query(query, params)

    def update_student_holyname(self, student_id, student_holyname):
        query = """
                UPDATE student
                SET student_holyname  = ?
                WHERE student_id = ?;
        """
        params = (student_holyname, student_id)
        return self.execute_query(query, params)

    def fetch_students_with_birthday(self, school_id):
        query = """
            SELECT *
            FROM student
            -- 将 student_birthday 时间戳转换为日期格式，然后提取月份
            WHERE strftime('%m', datetime(student_birthday, 'unixepoch')) = strftime('%m', 'now') and student_school_id = ?;
        """
        params = (school_id,)
        return self.fetch_query(query, params=params)

    def set_data_opera_type(self, student_id, opera_type):
        query = """
                UPDATE student
                SET opera_type = ?
                where student_id = ?;
        """
        params = (opera_type, student_id)
        return self.execute_query(query, params)

if __name__ == '__main__':
    with StudentDB(None) as db:
        # for i in range(10):
        #     for j in range(10):
        student_name = generate_chinese_name()
        student_gender = random.randint(0, 1)
        student_phonenum = "1310547" + str(random.randint(0, 99999))
        student_info = {
            "student_name": student_name,
            "student_gender": student_gender,
            "student_phonenum": student_phonenum,
            "student_holyname": "",
            "student_family_id": random.randint(1, 20),
            "student_school_id": 1,
        }
        idx = db.add_student(student_info)
        print(student_info)
        print(idx)
