import sqlite3


class DBInteraction:

    @staticmethod
    def connection(func):
        def wrapper(*args, **kwargs):
            connect = sqlite3.connect('./data/auto_db.db')
            cursor = connect.cursor()

            result = func(cursor=cursor, *args, **kwargs)
            connect.commit()
            cursor.close()
            connect.close()
            return result
        return wrapper
