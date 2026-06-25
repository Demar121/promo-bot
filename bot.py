import telebot
from telebot import types

TOKEN = "5513430886:AAHeNEQNCTA56RWvC6zrz4Gf1Xn5tjvJJDc"

bot = telebot.TeleBot(TOKEN)

users = {}

ADMIN_ID = 5017410644


@bot.message_handler(commands=['start'])
def start(message):
    users[message.chat.id] = {}

    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\nВведите свой игровой ник:"
    )


@bot.message_handler(func=lambda message: message.chat.id in users and "nick" not in users[message.chat.id])
def get_nick(message):
    users[message.chat.id]["nick"] = message.text

    bot.send_message(
        message.chat.id,
        "Отлично 👍\nТеперь напишите ваш сервер:"
    )


@bot.message_handler(func=lambda message: message.chat.id in users and "server" not in users[message.chat.id])
def get_server(message):
    users[message.chat.id]["server"] = message.text

    bot.send_message(
        message.chat.id,
        "Теперь отправьте скриншот 📸\nМожно отправить как фото или как файл."
    )


@bot.message_handler(content_types=['photo', 'document'])
def get_media(message):

    if message.chat.id not in users:
        bot.send_message(
            message.chat.id,
            "Нажмите /start"
        )
        return

    nick = users[message.chat.id].get("nick")
    server = users[message.chat.id].get("server")

    caption = (
        "🎁 Новая заявка!\n\n"
        f"👤 Ник: {nick}\n"
        f"🌐 Сервер: {server}\n"
        f"🆔 ID игрока: {message.chat.id}"
    )

    try:

        if message.content_type == "photo":

            bot.send_photo(
                ADMIN_ID,
                message.photo[-1].file_id,
                caption=caption
            )


        elif message.content_type == "document":

            bot.send_document(
                ADMIN_ID,
                message.document.file_id,
                caption=caption
            )


        bot.send_message(
            message.chat.id,
            "✅ Заявка отправлена!\nОжидайте проверки."
        )


    except Exception as e:

        print("Ошибка отправки админу:", e)

        bot.send_message(
            message.chat.id,
            "❌ Ошибка отправки, попробуйте ещё раз."
        )


bot.infinity_polling()
