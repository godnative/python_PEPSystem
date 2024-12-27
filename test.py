from DataBase.school_db import SchoolDb

if __name__ == '__main__':
    with SchoolDb() as db:
        result = db.fetch_school()
        print(result)
