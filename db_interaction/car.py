from db_interaction.db_interaction import DBInteraction as DBI


class Car:

    @staticmethod
    @DBI.connection
    def get_car_brand(cursor) -> list:
        car_list = cursor.execute(f"SELECT brand FROM car_brand")
        car_list = [item[0] for item in car_list]
        return car_list
