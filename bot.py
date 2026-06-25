import telebot
from telebot import types
from flask import Flask
from threading import Thread

TOKEN = "8738406014:AAFbF_Tbpj0EZMaO7-g72GUOhSNuxUYJ8Eo"

bot = telebot.TeleBot(TOKEN)

users = {}

ADMIN_ID = 5017410644


# ===== Render =====

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive"


def run():
    app.run(host="0.0.0.0", port=10000)


Thread(target=run).start()


# ===== Бот =====


@bot.message_handler(commands=['start'])
def start(message):

    users[message.chat.id] = {}

    bot.send_message(
        message.chat.id,
        "Привет! 👋\n\nВведите свой игровой ник:"
    )


@bot.message_handler(
    func=lambda message:
    message.chat.id in users
    and "nick" not in users[message.chat.id]
)
def get_nick(message):

    users[message.chat.id]["nick"] = message.text

    bot.send_message(
        message.chat.id,
        "Отлично 👍\nТеперь напишите ваш сервер:"
    )


@bot.message_handler(
    func=lambda message:
    message.chat.id in users
    and "server" not in users[message.chat.id]
)
def get_server(message):

    users[message.chat.id]["server"] = message.text

    bot.send_message(
        message.chat.id,
        "Теперь отправьте скриншот 📸"
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
        f"🆔 ID: {message.chat.id}"
    )


    markup = types.InlineKeyboardMarkup()

    approve = types.InlineKeyboardButton(
        "✅ Подтвердить",
        callback_data=f"approve_{message.chat.id}"
    )

    reject = types.InlineKeyboardButton(
        "❌ Отклонить",
        callback_data=f"reject_{message.chat.id}"
    )


    markup.add(approve, reject)


    if message.content_type == "photo":

        bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=caption,
            reply_markup=markup
        )


    elif message.content_type == "document":

        bot.send_document(
            ADMIN_ID,
            message.document.file_id,
            caption=caption,
            reply_markup=markup
        )


    bot.send_message(
        message.chat.id,
        "✅ Заявка отправлена!\nОжидайте проверки."
    )



# ===== Кнопки админа =====


@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    action, user_id = call.data.split("_")

    user_id = int(user_id)


    if action == "approve":

        bot.send_message(
            user_id,
            "✅ Ваша заявка проверена и одобрена!"
        )

        bot.answer_callback_query(
            call.id,
            "Подтверждено"
        )


    elif action == "reject":

        bot.send_message(
            user_id,
            "❌ Ваша заявка отклонена."
        )

        bot.answer_callback_query(
            call.id,
            "Отклонено"
        )


    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.id,
        reply_markup=None
    )



bot.infinity_polling()



      
