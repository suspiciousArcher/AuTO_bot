import telebot
from db_interaction.db_interaction import DBInteraction as DBI


DBI = DBI
bot = telebot.TeleBot(DBI.get_token())


@bot.message_handler(commands=['start'])
def start(message):
    # print(message)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id

    answer = DBI.registration(
        first_name=first_name,
        last_name=last_name,
        username=username,
        user_id=user_id
    )

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
