create
table
classes
(
    class_id   integer not null,
class_name TEXT not null
);

create
table
family
(
    family_id        integer not null
constraint family_pk
primary key autoincrement
constraint family_pk_2
unique,
family_name      TEXT not null
constraint family_pk_3
unique,
family_address   TEXT not null,
family_school_id integer not null,
family_notes     TEXT
);

create
table
school
(
    school_id      integer not null
constraint school_pk
primary key autoincrement
constraint school_pk_2
unique,
school_name    TEXT not null
constraint school_pk_3
unique,
school_date    DATE not null,
school_address TEXT not null,
school_info    TEXT
);

create
table
student
(
    student_id        integer not null
constraint student_pk
primary key autoincrement
constraint student_pk_2
unique,
student_gender    integer not null,
student_phonenum  TEXT,
student_holyname  TEXT,
student_family_id integer,
student_school_id integer not null,
student_name      TEXT not null
);

create
table
user
(
    user_id       integer not null
constraint user_pk
primary key autoincrement
constraint user_pk_2
unique,
user_name     TEXT not null,
user_type     integer not null,
user_password TEXT not null
);
