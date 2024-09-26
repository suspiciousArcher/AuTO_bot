from typing import Dict, Any

from db_interaction.db_interaction import DBInteraction as DBI


class Car:

    brand_id = None
    model_id = None
    body_id = None
    generation_id = None

    def set_user_car(self, message: dict) -> None:
        message_text = message.text
        user_id = message.from_user.id

        car = [value.strip() for value in message_text.split(',')]
        car_brand = car[0]
        car_model = car[1]
        car_body = car[2]
        car_generation = car[3]

        self.set_car_brand(user_id=user_id, brand=car_brand)
        self.set_car_model(user_id=user_id, model=car_model)


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
    def set_car_brand(self, *, cursor, user_id: int, brand: str) -> None:
        brand_list = self.get_car_brand(user_id=user_id)
        # print(brand_list)

        if brand in brand_list.values():
            self.brand_id = next(int(key) for key, value in brand_list.items() if value == brand)
            print(f'{self.brand_id=}')
            print(type(self.brand_id))
        else:
            cursor.execute(
                f"INSERT INTO car_brand (brand, user_id) VALUES ('{brand}', '{user_id}')"
            )

    @DBI.connection
    def set_car_model(self, *, cursor, user_id: int, model: str) -> None:
        model_list = self.get_car_brand(user_id=user_id)
        # print(model_list)

        if model in model_list.values():
            self.model_id = next(int(key) for key, value in model_list.items() if value == model)
            print(f'{self.model_id=}')
            print(type(self.model_id))
        else:
            cursor.execute(
                f"INSERT INTO car_model(model, user_id) VALUES ('{model}', '{user_id}')"
            )


