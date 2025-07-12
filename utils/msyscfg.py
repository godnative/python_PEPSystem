import os

AUTHOR = "堂区管理软件"
VERSION = "1.1"

SYSTEM_DATABASE_FILE_PATH = os.path.abspath("./DataBase/data.db").replace("\\", "/")
SYSTEM_DATABASE_BACKUP_FILE_PATH = os.path.abspath("./DataBase/backup/").replace("\\", "/")
