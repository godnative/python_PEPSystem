import sqlite3
import os
from sqlite3 import Error
import mysql.connector
from mysql.connector import errorcode
import pymysql

class DataBaseManage:
    def __init__(self, ):
        self.connection = None
        self.host = "localhost"
        self.user = "root"
        self.password = "123456"
        self.db_name = "my_database"

    def __enter__(self):
        self.connection = self.create_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def connect_to_mysql_and_create_db(self):
        """
        连接到MySQL服务器，如果数据库不存在则创建

        参数:
            host: MySQL服务器地址
            user: 用户名
            password: 密码
            self.db_name: 要连接/创建的数据库名
        """
        # 首先尝试连接到MySQL服务器（不指定数据库）
        try:
            cnx = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            print("成功连接到MySQL服务器")

            # 创建游标对象
            cursor = cnx.cursor()

            # 检查数据库是否存在
            cursor.execute(f"SHOW DATABASES LIKE '{self.db_name}'")
            result = cursor.fetchone()

            if result:
                print(f"数据库 '{self.db_name}' 已存在")
            else:
                # 创建数据库
                try:
                    cursor.execute(f"CREATE DATABASE {self.db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    print(f"成功创建数据库 '{self.db_name}'")
                except Error as err:
                    print(f"创建数据库失败: {err}")
                    return None

            # 关闭当前连接（不指定数据库的连接）
            cursor.close()
            cnx.close()

            # 重新连接，这次连接到指定的数据库
            try:
                cnx = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.db_name
                )
                print(f"成功连接到数据库 '{self.db_name}'")
                cnx.close()
                return True
            except pymysql.Error as err:
                print(f"连接到数据库失败: {err}")
                return None

        except pymysql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("认证失败: 用户名或密码错误")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("数据库不存在")
            else:
                print(f"连接MySQL服务器失败: {err}")
            return None

    def creat_all_database(self):
        # 创建users表的SQL语句
        """
        create table family
        (
            family_id int auto_increment,
            constraint family_pk
                primary key (family_id),
            constraint family_pk_2
                unique (family_id)
        );
        """
        sql_create_family_table = """ CREATE TABLE IF NOT EXISTS family (
                                        family_id        int  auto_increment not null ,
                                        family_name      VARCHAR(50)  not null,
                                        family_address   TEXT    not null,
                                        family_school_id int not null,
                                        family_notes     TEXT,
                                        operator         TEXT not null,
                                        opera_time       integer not null,
                                        opera_type       integer not null,
                                        constraint family_pk
                                            primary key (family_id),
                                        constraint family_pk_2
                                            unique (family_id, family_name)
                                    ); """

        # 创建products表的SQL语句
        sql_create_holyevent_table = """ CREATE TABLE IF NOT EXISTS holyevent (
                                        holyevent_id          integer auto_increment not null,
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
                                        opera_type            integer  not null,
                                       constraint holyevent_pk
                                                primary key (holyevent_id),
                                       constraint holyevent_pk_2
                                                unique (holyevent_id)
                                    ); """

        sql_create_parish_table = """ CREATE TABLE IF NOT EXISTS parish
                                    (
                                        parish_id       integer auto_increment not null,
                                        parish_name     VARCHAR(50)    not null,
                                        parish_date     DATE    not null,
                                        parish_address  TEXT    not null,
                                        parish_info     TEXT,
                                        parish_pic_path TEXT,
                                        parish_curadmin TEXT,
                                        constraint parish_pk
                                                primary key (parish_id),
                                        constraint parish_pk_2
                                                unique (parish_id,parish_name)
                                    ); """

        sql_create_student_table = """ CREATE TABLE IF NOT EXISTS student
                                    (
                                    student_id           integer auto_increment not null,
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
                                    opera_type           integer not null,
                                    constraint student_pk
                                        primary key (student_id),
                                    constraint student_pk_2
                                        unique (student_id)                                    
                                    ); """

        sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user
                                    (
                                        user_id       integer auto_increment not null,
                                        user_name     VARCHAR(50)    not null,
                                        user_type     integer not null,
                                        user_password TEXT    not null,
                                        user_authnum  integer not null,
                                        user_note     TEXT,
                                            constraint user_pk
                                                primary key (user_id),
                                            constraint user_pk_2
                                                unique (user_id, user_name)                                        
                                    ); """

        sql_create_user_log_table = """ CREATE TABLE IF NOT EXISTS user_log
                                    (
                                        user_log_id   integer auto_increment not null,
                                        user_id       integer not null,
                                        user_log_info TEXT,
                                        constraint user_log_pk
                                                primary key (user_log_id),
                                            constraint user_log_pk_2
                                                unique (user_log_id)
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
            query = """
                    SELECT COUNT(*) FROM user;
                    """
            user_cnt = self.fetch_query(query)[0]['COUNT(*)']

            if user_cnt == 0:
            # 关闭连接
            # 定义插入语句，将用户信息插入到 user 表的相应字段中
                query = """
                        INSERT INTO user (
                        user_name, user_password, user_type, user_authnum, user_note)
                        VALUES (%s, %s, %s, %s, %s)
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
        c = self.connection.cursor()
        try:
            c.execute(create_table_sql)
            print("表创建成功")
        except Error as e:
            print(e)
        finally:
            c.close()


    def create_connection(self):
        if self.connection is None:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
        return self.connection

    def fetch_query(self, query, single=False, params=None):
        result = None

        if self.connection:
            cursor = self.connection.cursor()
            try:
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
            finally:
                cursor.close()
        else:
            print('Connection failed')

        return result

    def execute_query(self, query, params):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                self.connection.commit()
                return True
            except Exception as e:
                print(f'Error: {e}')
                self.connection.rollback()
                return None
            finally:
                cursor.close()
        else:
            print('Connection failed')
        return None

    def execute_query_return_id(self, query, params):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, params)
                id = cursor.lastrowid
                self.connection.commit()
                return id
            except Exception as e:
                print(f'Error: {e}')
                self.connection.rollback()
                return None
            finally:
                cursor.close()
        else:
            print('Connection failed')
        return None

    def close_connection(self):
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    db = DataBaseManage()
    db.connect_to_mysql_and_create_db()
    db.creat_all_database()
