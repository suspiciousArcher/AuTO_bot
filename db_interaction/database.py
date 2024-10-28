import sqlite3


class DataBase:

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

    @staticmethod
    def get_sql_to_receive(*, name_properties: str, user_id: int = None) -> str:
        sql_dict = {
            'token': "SELECT `token` FROM `token_API`",
            'brand': f"SELECT id, brand FROM car_brand WHERE user_id = {user_id} OR user_id IS NULL",
            'model': f"SELECT id, model FROM car_model WHERE user_id = {user_id} OR user_id IS NULL",
            'model_range': f"SELECT id, model_range FROM car_model_range WHERE user_id = {user_id} OR user_id IS NULL",
            'body': f"SELECT id, body FROM car_body WHERE user_id = {user_id} OR user_id IS NULL",
            'generation': f"SELECT id, generation FROM car_generation WHERE user_id = {user_id} OR user_id IS NULL",
            'user': f"SELECT id FROM user WHERE user_id = {user_id}",
            'user_car': f"""SELECT id, user_id, brand_id, model_id, model_range_id, body_id, generation_id 
                                FROM user_car WHERE user_id = {user_id} """,
            'date': "SELECT id, date FROM date",
            'mileage': "SELECT id, mileage FROM mileage",
            'spare_part': "SELECT id, spare_part FROM spare_part",
            'date_mileage': "SELECT id, date_id, mileage_id FROM date_mileage"
        }

        return sql_dict[name_properties]

    @staticmethod
    def get_sql_to_write(*, name_table: str, data: dict) -> str:
        columns_list = [f'"{key}"' for key in data.keys()]
        properties_list = [f'"{value}"' for value in data.values()]

        columns = ', '.join(columns_list)
        properties = ', '.join(properties_list)

        sql = f"""
                           INSERT INTO '{name_table}' ({columns})
                           VALUES ({properties})
               """

        return sql
