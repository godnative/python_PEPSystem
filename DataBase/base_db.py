import sqlite3

db_path = "C:/Users/97895/Desktop/workspace/NewCode/python_PEPSystem/DataBase/data.db"


class DataBaseManage:
    def __init__(self, ):
        self.connection = None

    def __enter__(self):
        self.connection = self.create_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def create_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(db_path)
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
