from DataBase.base_db import DataBaseManage

class StudentDB(DataBaseManage):
    def fetch_students(self):
        # 定义查询语句
        query = """
               -- 查询学生表（student）中的所有字段，并关联班级表（classes），获取学生所属班级的名称
                SELECT s.*,              -- 查询 student 表中的所有字段
                       c.class_name      -- 查询 classes 表中的 class_name 字段（班级名称）
                FROM student s           -- 从 student 表中查询数据，给表取别名为 s
                JOIN classes c           -- 使用 INNER JOIN 连接 classes 表，给表取别名为 c
                ON s.class_id = c.class_id; -- 通过 student 表的 class_id 字段与 classes 表的 class_id 字段进行匹配
               """
        # 调用父类的 fetch_query 方法执行查询，并返回查询结果
        return self.fetch_query(query)

    def add_student(self, student):
        query = """
            INSERT INTO student (student_name, student_number, gender, class_id, chinese_score, math_score, english_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (student["student_name"], student["student_number"], student["gender"], student["class_id"],
                  student["chinese_score"], student["math_score"], student["english_score"])
        return self.execute_query(query, params)


if __name__ == '__main__':
    with StudentDB() as db:
        result = db.fetch_students()
        print(result)
