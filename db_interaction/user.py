from db_interaction.database import DataBase as DB


class User:
    user_id = None

    @DB.connection
    def get_user_car_info(self, *, cursor, user_id: int) -> tuple:
        cursor.execute(DB.get_sql_to_receive(name_properties='user_car', user_id=user_id))
        list_info = cursor.fetchall()
        return list_info

    @staticmethod
    @DB.connection
    def registration_user(cursor, first_name: str, last_name: str, username: str, user_id: int) -> str:
        try:
            cursor.execute(f"SELECT `user_id` FROM `users` WHERE user_id = {user_id}")
            result = cursor.fetchone()

            if result is not None:
                answer = 'С возвращением 🤝'
            else:
                answer = 'Добро пожаловать в клуб 🎉'
                cursor.execute(
                    f"INSERT INTO `users` (`first_name`, `last_name`, `username`, `user_id`) \
                          VALUES ('{first_name}', '{last_name}', '{username}', {user_id})")

            return answer

        except:
            answer = 'Не предвиденная ошибка 🤷 \nПопробуйте позже 🫠 '
            return answer

    @DB.connection
    def set_user_car(self, *, cursor, message: dict, bot: object, car: object) -> None:
        message_text = message.text
        user_id = message.from_user.id

        data_car = [value.strip() for value in message_text.split(',')]
        if len(data_car) != 5:
            bot.send_message(message.chat.id,
                             "Ошибка: неверно указаны параметры автомобиля. \
                             \nЗаново используйте функцию /addcar и ведите данные в формате: \
                             \n'Марка, Модель, Модельный ряд, Тип кузова, Поколение'")
            return
        car_brand, car_model, car_model_range, car_body, car_generation = data_car

        car.set_car_info(user_id=user_id, name_properties='brand', properties=car_brand)
        car.set_car_info(user_id=user_id, name_properties='model', properties=car_model)
        car.set_car_info(user_id=user_id, name_properties='model_range', properties=car_model_range)
        car.set_car_info(user_id=user_id, name_properties='body', properties=car_body)
        car.set_car_info(user_id=user_id, name_properties='generation', properties=car_generation)

        answer = self.set_user_car_info(user_id=user_id, car=car)

        bot.send_message(message.chat.id, answer)

    @DB.connection
    def set_user_car_info(self, *, cursor, user_id: int, car: object) -> str:  # Перенести в User
        answer = None

        list_info = self.get_user_car_info(user_id=user_id)
        car_obj_dict = (
            user_id,
            car.brand_id,
            car.model_id,
            car.model_range_id,
            car.body_id,
            car.generation_id
        )

        if any(car_obj_dict == item[1:] for item in list_info):
            answer = 'Авто уже зарегестрировано!'
        else:
            cursor.execute(
                DB.get_sql_to_write(
                    name_table="user_car",
                    data={
                        "user_id": f'{user_id}',
                        "brand_id": f'{car.brand_id}',
                        "model_id": f'{car.model_id}',
                        "model_range_id": f'{car.model_range_id}',
                        "body_id": f'{car.body_id}',
                        "generation_id": f'{car.generation_id}'
                    }
                )
            )
            answer = 'Авто зарегестрировано!'

        return answer
