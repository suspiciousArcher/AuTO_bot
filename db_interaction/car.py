from db_interaction.db_interaction import DBInteraction as DBI
from db_interaction.bot import Bot


class Car:
    brand_id = None
    model_id = None
    model_range_id = None
    body_id = None
    generation_id = None

    @staticmethod
    def get_sql_to_receive(*, name_properties: str, user_id: int) -> str:
        sql_dict = {
            'brand': f"SELECT id, brand FROM car_brand WHERE user_id = {user_id} OR user_id IS NULL",
            'model': f"SELECT id, model FROM car_model WHERE user_id = {user_id} OR user_id IS NULL",
            'model_range': f"SELECT id, model_range FROM car_model_range WHERE user_id = {user_id} OR user_id IS NULL",
            'body': f"SELECT id, body FROM car_body WHERE user_id = {user_id} OR user_id IS NULL",
            'generation': f"SELECT id, generation FROM car_generation WHERE user_id = {user_id} OR user_id IS NULL",
            'user_car': f"""SELECT id, user_id, brand_id, model_id, model_range_id, body_id, generation_id 
                            FROM user_car WHERE user_id = {user_id} """
        }

        return sql_dict[name_properties]

    # @staticmethod
    # def get_sql_to_write(*, name_table: str, name_columns: str, properties: str) -> str:
    #     sql = f"""
    #                 INSERT INTO '{name_table}' ('{name_columns}')
    #                 VALUES ('{properties}')
    #     """
    #
    #     return sql

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
        # print(sql)

        return sql



    #  Переписать все get и set методы в два. 1 - set, 1 - get с доп параметрами "имя таблицы"-"поля"-"значения".
    #  set_user_car - оставить.

    @DBI.connection
    def get_car_info(self, *, cursor, user_id: int, name_properties: str) -> dict:
        cursor.execute(self.get_sql_to_receive(name_properties=name_properties, user_id=user_id))
        list_info = cursor.fetchall()
        list_info = dict(list_info)
        return list_info

    @DBI.connection
    def get_user_car_info(self, *, cursor, user_id: int, name_properties: str) -> tuple:
        cursor.execute(self.get_sql_to_receive(name_properties=name_properties, user_id=user_id))
        list_info = cursor.fetchone()
        # list_info = dict(list_info)
        return list_info

    """__________________________________________SET методы__________________________________________________"""

    @DBI.connection
    def set_user_car(self, *, cursor, message: dict, bot: object) -> None:
        message_text = message.text
        user_id = message.from_user.id

        car = [value.strip() for value in message_text.split(',')]
        car_brand = car[0]
        car_model = car[1]
        car_model_range = car[2]
        car_body = car[3]
        car_generation = car[4]

        self.set_car_info(user_id=user_id, name_properties='brand', properties=car_brand)
        self.set_car_info(user_id=user_id, name_properties='model', properties=car_model)
        self.set_car_info(user_id=user_id, name_properties='model_range', properties=car_model_range)
        self.set_car_info(user_id=user_id, name_properties='body', properties=car_body)
        self.set_car_info(user_id=user_id, name_properties='generation', properties=car_generation)

        answer = self.set_user_car_info(user_id=user_id)

        bot.send_message(message.chat.id, answer)

    @DBI.connection
    def set_car_info(self, *, cursor, user_id: int, name_properties: str, properties: str) -> None:
        list_info = self.get_car_info(name_properties=name_properties, user_id=user_id)
        name_atr = f'{name_properties}_id'

        if properties in list_info.values():  # Логику проверки вынести в отдельный метод
            setattr(self, name_atr, next(int(key) for key, value in list_info.items() if value == properties))
            # print(f'{self.brand_id=}')
            # print(type(self.brand_id))
        else:
            print('в если set_car_info')
            print(f'{name_properties=}')
            cursor.execute(
                self.get_sql_to_write(
                    name_table=f'car_{name_properties}',
                    data={
                        f"{name_properties}": f"{properties}"
                    }
                    # name_columns=name_properties,
                    # properties=properties
                )
            )
            row_id = cursor.lastrowid
            setattr(self, name_atr, row_id)

    @DBI.connection
    def set_user_car_info(self, *, cursor, user_id: int) -> str:  # Поправить дублирование записей
        answer = None

        list_info = self.get_user_car_info(name_properties='user_car', user_id=user_id)
        car_obj_dict = (
            user_id,
            self.brand_id,
            self.model_id,
            self.model_range_id,
            self.body_id,
            self.generation_id
        )

        if list_info[1:] == car_obj_dict:
            # print("Зарегано")
            answer = 'Авто уже зарегестрировано!'
        else:
            cursor.execute(
                self.get_sql_to_write(
                    name_table="user_car",
                    data={
                        "user_id": f'{user_id}',
                        "brand_id": f'{self.brand_id}',
                        "model_id": f'{self.model_id}',
                        "model_range_id": f'{self.model_range_id}',
                        "body_id": f'{self.body_id}',
                        "generation_id": f'{self.generation_id}'
                    }
                    # name_columns='user_id, brand_id, model_id, model_range_id, body_id, generation_id',
                    # properties=f'{user_id}, {self.brand_id}, {self.model_id}, \
                    #             {self.model_range_id}, {self.body_id}, {self.generation_id}'
                )
            )
            answer = 'Авто зарегестрировано!'

        return answer
