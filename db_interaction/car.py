from typing import Dict, Any

from db_interaction.db_interaction import DBInteraction as DBI


class Car:
    brand_id = None
    model_id = None
    model_range_id = None
    body_id = None
    generation_id = None

    brand_model_id = None
    brand_model_model_range_id = None
    brand_model_body_id = None
    brand_model_body_generation_id = None

    #  Переписать все get и set методы в два. 1 - set, 1 - get с доп параметрами "имя таблицы"-"поля"-"значения".
    #  set_user_car - оставить.

    @staticmethod
    @DBI.connection
    def get_car_brand(*, cursor, user_id: int) -> dict:
        car_list = cursor.execute(
            f"SELECT id, brand FROM car_brand WHERE user_id = {user_id} OR user_id IS NULL"
        )
        car_list = dict(car_list)
        # car_list = [item[0] for item in car_list]
        return car_list

    @staticmethod
    @DBI.connection
    def get_car_model(*, cursor, user_id: int) -> dict:
        model_list = cursor.execute(
            f"SELECT id, model FROM car_model WHERE user_id = {user_id} OR user_id IS NULL"
        )
        model_list = dict(model_list)
        # model_list = [item[0] for item in model_list]
        return model_list

    @staticmethod
    @DBI.connection
    def get_car_model_range(*, cursor, user_id: int) -> dict:
        model_range_list = cursor.execute(
            f"SELECT id, model_range FROM car_model_range WHERE user_id = {user_id} OR user_id IS NULL"
        )
        model_range_list = dict(model_range_list)
        # model_range_list = [item[0] for item in model_range_list]
        return model_range_list

    @staticmethod
    @DBI.connection
    def get_car_body(*, cursor, user_id: int) -> dict:
        body_list = cursor.execute(
            f"SELECT id, body FROM car_body WHERE user_id = {user_id} OR user_id IS NULL"
        )
        body_list = dict(body_list)
        return body_list

    @staticmethod
    @DBI.connection
    def get_car_generation(*, cursor, user_id: int) -> dict:
        generation_list = cursor.execute(
            f"SELECT id, generation FROM car_generation WHERE user_id = {user_id} OR user_id IS NULL"
        )
        generation_list = dict(generation_list)
        return generation_list

    """__________________________________________SET методы__________________________________________________"""

    @DBI.connection
    def set_user_car(self, *, cursor, message: dict) -> None:
        message_text = message.text
        user_id = message.from_user.id

        car = [value.strip() for value in message_text.split(',')]
        car_brand = car[0]
        car_model = car[1]
        car_model_range = car[2]
        car_body = car[3]
        car_generation = car[4]

        self.set_car_brand(user_id=user_id, brand=car_brand)
        self.set_car_model(user_id=user_id, model=car_model)
        self.set_car_model_range(user_id=user_id, model_range=car_model_range)
        self.set_car_body(user_id=user_id, body=car_body)
        self.set_car_generation(user_id=user_id, generation=car_generation)

        self.set_car_brand_model()

    @DBI.connection
    def set_car_brand(self, *, cursor, user_id: int, brand: str) -> None:
        brand_list = self.get_car_brand(user_id=user_id)
        # print(brand_list)

        if brand in brand_list.values():  # Логику проверки вынести в отдельный метод
            self.brand_id = next(int(key) for key, value in brand_list.items() if value == brand)
            # print(f'{self.brand_id=}')
            # print(type(self.brand_id))
        else:
            cursor.execute(
                f"INSERT INTO car_brand (brand) VALUES ('{brand}')"
            )

    @DBI.connection
    def set_car_model(self, *, cursor, user_id: int, model: str) -> None:
        model_list = self.get_car_model(user_id=user_id)
        # print(model_list)

        if model in model_list.values():
            self.model_id = next(int(key) for key, value in model_list.items() if value == model)
            # print(f'{self.model_id=}')
            # print(type(self.model_id))
        else:
            cursor.execute(
                f"INSERT INTO car_model (model) VALUES ('{model}')"
            )

    @DBI.connection
    def set_car_model_range(self, *, cursor, user_id: int, model_range: str) -> None:
        model_range_list = self.get_car_model_range(user_id=user_id)
        # print(model_range_list)

        if model_range in model_range_list.values():
            self.model_range_id = next(int(key) for key, value in model_range_list.items() if value == model_range)
            # print(f'{self.model_id=}')
            # print(type(self.model_id))
        else:
            cursor.execute(
                f"INSERT INTO car_model_range (model_range) VALUES ('{model_range}')"
            )

    @DBI.connection
    def set_car_body(self, *, cursor, user_id: int, body: str) -> None:
        body_list = self.get_car_body(user_id=user_id)
        # print(body_list)

        if body in body_list.values():
            self.body_id = next(int(key) for key, value in body_list.items() if value == body)
            # print(f'{self.body_id=}')
            # print(type(self.body_id))
        else:
            cursor.execute(
                f"INSERT INTO car_body (body) VALUES ('{body}')"
            )

    @DBI.connection
    def set_car_generation(self, *, cursor, user_id: int, generation: str) -> None:
        generation_list = self.get_car_generation(user_id=user_id)
        # print(generation_list)

        if generation in generation_list.values():
            self.generation_id = next(int(key) for key, value in generation_list.items() if value == generation)
            # print(f'{self.generation_id=}')
            # print(type(self.generation_id))
        else:
            cursor.execute(
                f"INSERT INTO car_generation (generation) VALUES ('{generation}')"
            )

    @DBI.connection
    def set_car_brand_model(self, *, cursor) -> None:  # получение связей между таблицами реализовать более логично
        brand_model_list = cursor.execute(
            f"SELECT id FROM car_brand_model WHERE brand_id = {self.brand_id} AND model_id = {self.model_id}"
        )

        if bool(tuple(brand_model_list)):
            self.brand_model_id = tuple(brand_model_list)[0][0]
        else:
            brand_model_list = cursor.execute(
                f"""
                        INSERT INTO car_brand_model (brand_id, model_id)
                        VALUES ({self.brand_id}, {self.model_id})
                    """
            )
            self.brand_model_id = cursor.lastrowid
            # print(self.brand_model_id)