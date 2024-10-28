from db_interaction.database import DataBase as DB
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
    MESSAGE_ADD_CAR = '''
    Для регистрации автомобиля отправте сообщением его Марку, Модель, Модельный ряд, Тип кузова и Поколение.\
    \nВ качестве разделителя используйте ",". \
    \nЕсли вы не знаете/не хотите указывать один из параметров используйте символ "-".
    '''
    MESSAGE_GET_CAR = '''
    
    '''

    @staticmethod
    @DB.connection
    def get_token(cursor) -> str:
        cursor.execute(DB.get_sql_to_receive(name_properties='token'))
        result = cursor.fetchone()
        return result[0] if result else None


    # def registration_car(self, message: dict) -> None:
    #     text = message.text
    #     print(text)

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
