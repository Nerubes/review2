import random

import telebot as tb

import const
import database
import parse

bot = tb.TeleBot(const.TOKEN)


@bot.message_handler(content_types=['text'])
def get_message(message):
    """
    Получает и обрабатывает сообщение от пользователя
    :param message: сообщение
    """
    send_message(message.text, message.from_user.id)


def send_message(message_text, user_id):
    """
    Обрабатывает полученное сообщение и отправляет ответ
    :param message_text: текст сообщения
    :param user_id: id пользователя
    """
    commands = message_text.split()
    if commands[0] == "/help":
        bot.send_message(user_id, "/top random")
        bot.send_message(user_id, "/top [number]")
        bot.send_message(user_id, "/new")
        bot.send_message(user_id, "/random")
        bot.send_message(user_id, "/search [your text]")
        bot.send_message(user_id,
                         "/search_genre_top [детектив/комедия/пародия/мехи/повседневность/романтика,/фантастика/этти]")
        bot.send_message(user_id, "/subscribe")
        bot.send_message(user_id, "/unsubscribe")
    elif len(commands) == 2 and commands[0] == "/top":
        if commands[1] == "random":
            res = parse.parse_top(100)
            answ = res[random.randrange(100)]
            bot.send_photo(user_id, answ[0], answ[1] + ": " + answ[2])
        elif commands[1].isnumeric():
            res = parse.parse_top(int(commands[1]))
            for top_anim in res:
                bot.send_photo(user_id, top_anim[0], top_anim[1] + ": " + top_anim[2])
        else:
            bot.send_message(user_id, "Invalid Command. Type /help for all commands.")
    elif commands[0] == "/new":
        res = parse.parse_new(5)
        for new in res:
            bot.send_photo(user_id, new[0], new[1] + ": " + new[2])
    elif commands[0] == "/random":
        res = parse.parse_random()
        bot.send_photo(user_id, res[0], res[1] + ": " + res[2])
    elif len(commands) >= 2 and commands[0] == "/search":
        ser = ""
        for word in range(1, len(commands)):
            ser = ser + commands[word] + "_"
        res = parse.search(ser)
        if res == []:
            bot.send_message(user_id, "Nothing was found.")
        else:
            for anim in res:
                bot.send_photo(user_id, anim[0], anim[1] + ": " + anim[2])
    elif len(commands) >= 2 and commands[0] == "/search_genre_top":
        index = parse.get_index(commands[1])
        if not index:
            bot.send_message(user_id, "Invalid genre.")
        else:
            res = parse.search_genre_top(index)
            for i in res:
                bot.send_photo(user_id, i[0], i[1] + ": " + i[2])
    elif commands[0] == "/subscribe":
        database.subscribe(user_id, const.DATABASE)
        print(user_id)
        bot.send_message(user_id, "You were subscribed.")
    elif commands[0] == "/unsubscribe":
        database.unsubscribe(user_id, const.DATABASE)
        bot.send_message(user_id, "You were unsubscribed.")
    elif commands[0] == "//send" and const.ADMIN == user_id:
        ser = ""
        for word in range(1, len(commands)):
            ser = ser + commands[word] + " "
        for sub in database.get_all_subs(const.DATABASE):
            bot.send_message(sub[0], ser)
    else:
        bot.send_message(user_id, "Invalid Command. Type /help for all commands.")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
