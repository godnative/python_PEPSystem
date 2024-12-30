from DataBase.base_db import DataBaseManage


class StudentDB(DataBaseManage):
    def __init__(self):
        super().__init__()

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
                                    student_family_id, student_school_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (student["student_name"], student["student_gender"], student["student_phonenum"],
                  student["student_holyname"], student["student_family_id"], student["student_school_id"])
        return self.execute_query(query, params)


if __name__ == '__main__':
    with StudentDB("./data.db") as db:
        # for i in range(10):
        #     for j in range(10):
        #         student_name = generate_chinese_name()
        #         student_gender = random.randint(0, 1)
        #         student_phonenum = "1310547" + str(random.randint(0, 99999))
        #         student_info = {
        #             "student_name": student_name,
        #             "student_gender": student_gender,
        #             "student_phonenum": student_phonenum,
        #             "student_holyname": "",
        #             "student_family_id": j + 1,
        #             "student_school_id": 0,
        #         }
        #         db.add_student(student_info)
        result = db.fetch_students()
        print(result)
