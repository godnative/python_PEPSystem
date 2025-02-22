from DataBase.family_db import FamilyDB

if __name__ == '__main__':
    with FamilyDB() as db:
        print(db.fetch_family_with_school_id(2))
