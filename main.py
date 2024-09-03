import telebot
from db_interaction.bot import Bot
from db_interaction.car import Car


bot = Bot(Bot.get_token())


@bot.message_handler(commands=['start'])
def start(message):
    # print(message)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id

    answer = bot.registration(
        first_name=first_name,
        last_name=last_name,
        username=username,
        user_id=user_id
    )

    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['help'])
def assist(message):
    bot.send_message(message.chat.id, bot.MESSAGE_HELP)

@bot.message_handler(commands=['addcar'])
def add_car(message):
    bot.send_message(message.chat.id, bot.MESSAGE_ADDCAR,
                     reply_markup=bot.create_reply_markup(Car.get_car_brand(), 3))


bot.polling(none_stop=True)
