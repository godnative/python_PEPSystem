import sqlite3
import os
from sqlite3 import Error



class DataBaseManage:
    def __init__(self, ):
        self.connection = None
        if os.path.exists("./DataBase/data.db"):
            self.db_path = "./DataBase/data.db"
        elif os.path.exists("../DataBase/data.db"):
            self.db_path = "../DataBase/data.db"
        elif os.path.exists("./data.db"):
            self.db_path = "./data.db"
        else:
            self.db_path = "./data.db"

        self.creat_all_database()

    def __enter__(self):
        self.connection = self.create_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def creat_all_database(self):
        # 创建users表的SQL语句
        if os.path.exists(self.db_path):
            return
        sql_create_family_table = """ CREATE TABLE IF NOT EXISTS family (
                                        family_id        integer not null
                                            constraint family_pk
                                                primary key autoincrement
                                            constraint family_pk_2
                                                unique,
                                        family_name      TEXT    not null
                                            constraint family_pk_3
                                                unique,
                                        family_address   TEXT    not null,
                                        family_school_id integer not null,
                                        family_notes     TEXT,
                                        operator         TEXT not null,
                                        opera_time       integer not null,
                                        opera_type       integer not null
                                    ); """

        # 创建products表的SQL语句
        sql_create_holyevent_table = """ CREATE TABLE IF NOT EXISTS holyevent (
                                        holyevent_id          integer not null
                                            constraint holyevent_pk
                                                primary key autoincrement
                                            constraint holyevent_pk_2
                                                unique,
                                        holyevent_type        integer not null,
                                        holyevent_date        INT     not null,
                                        holyevent_witness     TEXT,
                                        holyevent_implementer TEXT    not null,
                                        holyevent_p1_id       integer not null,
                                        holyevent_p2_id       integer,
                                        holyevent_note        TEXT,
                                        holyevent_school_id   integer not null,
                                        operator              TEXT not null,
                                        opera_time            integer not null,
                                        opera_type            integer  not null
                                    ); """

        sql_create_parish_table = """ CREATE TABLE IF NOT EXISTS parish
                                    (
                                        parish_id       integer not null
                                            constraint parish_pk
                                                primary key autoincrement
                                            constraint parish_pk_2
                                                unique,
                                        parish_name     TEXT    not null
                                            constraint parish_pk_3
                                                unique,
                                        parish_date     DATE    not null,
                                        parish_address  TEXT    not null,
                                        parish_info     TEXT,
                                        parish_pic_path TEXT,
                                        parish_curadmin TEXT
                                    ); """

        sql_create_student_table = """ CREATE TABLE IF NOT EXISTS student
                                    (
                                    student_id           integer not null
                                        constraint student_pk
                                            primary key autoincrement
                                        constraint student_pk_2
                                            unique,
                                    student_gender       integer not null,
                                    student_phonenum     TEXT,
                                    student_holyname     TEXT,
                                    student_family_id    integer,
                                    student_school_id    integer not null,
                                    student_name         TEXT    not null,
                                    student_identity_num TEXT,
                                    student_birthday     integer,
                                    student_note         TEXT,
                                    operator             TEXT not null,
                                    opera_time           integer not null,
                                    opera_type           integer not null
                                    ); """

        sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user
                                    (
                                        user_id       integer not null
                                            constraint user_pk
                                                primary key autoincrement
                                            constraint user_pk_2
                                                unique,
                                        user_name     TEXT    not null
                                            constraint user_pk_3
                                                unique,
                                        user_type     integer not null,
                                        user_password TEXT    not null,
                                        user_authnum  integer not null,
                                        user_note     TEXT
                                    ); """

        sql_create_user_log_table = """ CREATE TABLE IF NOT EXISTS user_log
                                    (
                                        user_log_id   integer not null
                                            constraint user_log_pk
                                                primary key autoincrement
                                            constraint user_log_pk_2
                                                unique,
                                        user_id       integer not null,
                                        user_log_info TEXT
                                    ); """

        conn = self.create_connection()

        # 创建表
        if conn is not None:
            # 创建users表
            self.create_table(sql_create_family_table)
            self.create_table(sql_create_holyevent_table)
            self.create_table(sql_create_parish_table)
            self.create_table(sql_create_student_table)
            self.create_table(sql_create_user_table)
            self.create_table(sql_create_user_log_table)

            # 可以在这里添加插入示例数据的代码
            # insert_data(conn)

            # 关闭连接
            # 定义插入语句，将用户信息插入到 user 表的相应字段中
            query = """
                    INSERT INTO user (
                    user_name, user_password, user_type, user_authnum, user_note)
                    VALUES (?, ?, ?, ?, ?)
                    """
            # 从 user_info 字典中提取各字段的值作为查询参数
            params = ('admin',
                      'admin123',
                      0,
                      32767,
                      '管理员'
                      )
            # 调用父类的 execute_query 方法执行插入操作
            self.execute_query(query, params=params)
            conn.close()

        else:
            print("无法创建数据库连接")
    def create_table(self, create_table_sql):
        """ 从SQL语句创建表 """
        try:
            c = self.connection.cursor()
            c.execute(create_table_sql)
            print("表创建成功")
        except Error as e:
            print(e)

    def create_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def fetch_query(self, query, single=False, params=None):
        result = None

        if self.connection:
            try:
                cursor = self.connection.cursor()
                if params is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                columns = [column[0] for column in cursor.description]
                if single:
                    result = cursor.fetchone()
                    result = dict(zip(columns, result))
                else:
                    result = cursor.fetchall()
                    result = [dict(zip(columns, row)) for row in result]
            except Exception as e:
                print(e)
        else:
            print('Connection failed')

        return result

    def execute_query(self, query, params):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                self.connection.commit()
                return True
            except Exception as e:
                print(f'Error: {e}')
                self.connection.rollback()
                return None
        else:
            print('Connection failed')
        return None

    def execute_query_return_id(self, query, params):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                id = cursor.lastrowid
                self.connection.commit()
                return id
            except Exception as e:
                print(f'Error: {e}')
                self.connection.rollback()
                return None
        else:
            print('Connection failed')
        return None

    def close_connection(self):
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    with DataBaseManage() as db:
        pass
