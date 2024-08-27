import sqlite3


class DBInteraction:

    @staticmethod
    def connection(func):
        def wrapper(*args, **kwargs):
            connect = sqlite3.connect('./data/auto_db.db')
            cursor = connect.cursor()

            result = func(cursor, *args, **kwargs)
            connect.commit()
            cursor.close()
            connect.close()
            return result
        return wrapper

    @staticmethod
    @connection
    def get_token(cursor):
        cursor.execute("SELECT `token` FROM `token_API`")
        result = cursor.fetchone()
        return result[0] if result else None

    @staticmethod
    @connection
    def registration(cursor, first_name, last_name, username, user_id):
        try:
            cursor.execute(f"SELECT `user_id` FROM `users` WHERE user_id = {user_id}")
            result = cursor.fetchone()

            if result is not None:
                answer = 'Вы уже наш пользователь 🤝'
            else:
                answer = 'Вы зарегистрированны 🎉'
                cursor.execute(
                    f"INSERT INTO `users` (`first_name`, `last_name`, `username`, `user_id`) \
                    VALUES ('{first_name}', '{last_name}', '{username}', {user_id})")

            return answer

        except:
            answer = 'Не предвиденная ошибка 🤷 \nПопробуйте позже 🫠 '
            return answer
