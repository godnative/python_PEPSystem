import os

CUR_SYS_TYPE = 0  # 0 为服务端 1 为客户端无本地存储
if CUR_SYS_TYPE == 0:
    AUTHOR = "堂区管理软件"
    VERSION = "1.1"

    SYSTEM_DATABASE_FILE_PATH = os.path.abspath("./DataBase/data.db").replace("\\", "/")
    SYSTEM_DATABASE_BACKUP_FILE_PATH = os.path.abspath("./DataBase/backup/").replace("\\", "/")
else:
    AUTHOR = "堂区管理软件-客户端"
    VERSION = "1.1"
