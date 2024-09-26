from typing import Dict, Any

from db_interaction.db_interaction import DBInteraction as DBI


class Car:

    brand_id = None
    model_id = None
    body_id = None
    generation_id = None

    @staticmethod
    @DBI.connection
    def get_car_brand(*, cursor, user_id: int) -> dict:
        car_list = cursor.execute(
            f"SELECT id, brand FROM car_brand WHERE user_id = {user_id} OR user_id IS NULL"
        )
        car_list = dict(car_list)
        # car_list = [item[0] for item in car_list]
        return car_list

    @DBI.connection
    def set_car_brand(self, *, cursor, user_id: int, brand: str):
        brand_list = self.get_car_brand(user_id=user_id)
        if brand in brand_list.values():
            self.brand_id = next((key for key, value in brand_list.items() if value == brand), None)
            print(self.brand_id)


    @DBI.connection
    def get_car_model(self, *, cursor, user_id: int) -> dict[Any, Any] | dict[str, Any] | dict[str, str]:
        model_list = cursor.execute(
            f"""SELECT cm.model
                FROM car_brand_model cbm
                JOIN car_brand cb ON cb.id = cbm.brand_id 
                JOIN car_model cm ON cm.id = cbm.model_id
                WHERE cm.user_id = {user_id} OR cm.user_id IS NULL
                AND cb.id = '{self.brand_id}'
            """
        )
        model_list = dict(model_list)
        # model_list = [item[0] for item in model_list]
        return model_list

    @staticmethod
    @DBI.connection
    def get_car_body(cursor, user_id: int) -> list:
        body_list = cursor.execute(
            f"SELECT body FROM car_body WHERE user_id = {user_id} OR user_id IS NULL"
        )
        body_list = [item[0] for item in body_list]
        return body_list

    @staticmethod
    @DBI.connection
    def get_car_generation(cursor, user_id: int) -> list:
        generation_list = cursor.execute(
            f"SELECT generation FROM car_generation WHERE user_id = {user_id} OR user_id IS NULL"
        )
        generation_list = [item[0] for item in generation_list]
        return generation_list
