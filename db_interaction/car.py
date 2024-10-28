from db_interaction.database import DataBase as DB


class Car:
    brand_id = None
    model_id = None
    model_range_id = None
    body_id = None
    generation_id = None

    user_car_id = None


    #  Переписать все get и set методы в два. 1 - set, 1 - get с доп параметрами "имя таблицы"-"поля"-"значения".
    #  set_user_car - оставить.

    @DB.connection
    def get_car_info(self, *, cursor, user_id: int, name_properties: str) -> dict:
        cursor.execute(DB.get_sql_to_receive(name_properties=name_properties, user_id=user_id))
        list_info = cursor.fetchall()
        list_info = dict(list_info)
        return list_info

    """__________________________________________SET методы__________________________________________________"""


    @DB.connection
    def set_car_info(self, *, cursor, user_id: int, name_properties: str, properties: str) -> None:
        list_info = self.get_car_info(name_properties=name_properties, user_id=user_id)
        name_atr = f'{name_properties}_id'

        if properties in list_info.values():  # Логику проверки вынести в отдельный метод
            setattr(self, name_atr, next(int(key) for key, value in list_info.items() if value == properties))
        else:
            cursor.execute(
                DB.get_sql_to_write(
                    name_table=f'car_{name_properties}',
                    data={
                        f"{name_properties}": f"{properties}"
                    }
                )
            )
            row_id = cursor.lastrowid
            setattr(self, name_atr, row_id)

