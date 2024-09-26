from db_interaction.db_interaction import DBInteraction as DBI
from telebot import TeleBot, types


class Bot(TeleBot):
    """
    В дальнейшем перенести все фразы бота в базу и тянуть через метод
    """
    MESSAGE_HELP = '''
    /addcar - добавить информацию о автомобиле\
    \n/updatecar - обновить информацию о уже внесенном автомобиле\
    \n/deletecar - удалить автомобиль и информацию о нем
    '''
    MESSAGE_ADD_BRAND = 'Укажите марку автомобиля'
    MESSAGE_ADD_MODEL = 'Укажите модель автомобиля'
    MESSAGE_ADD_BODY = 'Укажите тип кузова автомобиля'
    MESSAGE_ADD_GENERATION = 'Укажите поколение автомобиля'
    MESSAGE_ADD_CAR = '''
    Для регистрации автомобиля отправте сообщением его Марку, Модель, Тип кузова и Поколение сообщением.\
    \nВ качестве разделителя используйте запятую.
    '''

    @staticmethod
    @DBI.connection
    def get_token(cursor) -> str:
        cursor.execute("SELECT `token` FROM `token_API`")
        result = cursor.fetchone()
        return result[0] if result else None

    @staticmethod
    @DBI.connection
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

    def registration_car(self, message: dict) -> None:
        text = message.text
        print(text)

    # @staticmethod
    # def create_reply_markup(options_ist: dict, items_in_row: int = 3):
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     options_ist = [value for value in options_ist.values()]
    #
    #     rows = [options_ist[i:i + items_in_row] if (i + items_in_row) < len(options_ist)
    #             else options_ist[i:len(options_ist)]
    #             for i in range(0, len(options_ist), items_in_row)]
    #
    #     for row in rows:
    #         buttons = [types.KeyboardButton(text=text) for text in row]
    #         markup.add(*buttons)
    #
    #     return markup
    #
    # def close_reply_markup(self, message, text):
    #     self.send_message(message.chat.id, text, reply_markup=types.ReplyKeyboardRemove())
