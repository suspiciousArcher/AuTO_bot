from db_interaction.db_interaction import DBInteraction as DBI


class SparePart:

    def get_sql_to_receive(*, name_properties: str, user_id: int) -> str:
        sql_dict = {
            'date': "SELECT id, date FROM date",
            'mileage': "SELECT id, mileage FROM mileage",
            'spare_part': "SELECT id, spare_part FROM spare_part",
            'date_mileage': "SELECT id, date_id, mileage_id FROM date_mileage"
        }

        return sql_dict[name_properties]