import os
import sqlite3
from sqlite3 import Error

from DataBase.user_db import UserDB




def creat_all_database():
    # 创建users表的SQL语句
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
    # 创建数据库连接

    conn = create_connection(db_path)

    # 创建表
    if conn is not None:
        # 创建users表
        create_table(conn, sql_create_family_table)
        create_table(conn, sql_create_holyevent_table)
        create_table(conn, sql_create_parish_table)
        create_table(conn, sql_create_student_table)
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_user_log_table)

        # 可以在这里添加插入示例数据的代码
        # insert_data(conn)

        # 关闭连接
        conn.close()
        with UserDB() as db:
            db.add_user({'user_name': 'admin', 'user_password': 'admin123', 'user_type': 0, 'user_authnum': 32767,
                         'user_note': '管理员'})

    else:
        print("无法创建数据库连接")



if __name__ == '__main__':
    creat_all_database()