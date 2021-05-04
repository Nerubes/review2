import random

import telebot as tb

import const
import database
import parse

bot = tb.TeleBot(const.TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    commands = message.text.split()
    if commands[0] == "/help":
        bot.send_message(message.from_user.id, "/top random")
        bot.send_message(message.from_user.id, "/top [number]")
        bot.send_message(message.from_user.id, "/new")
        bot.send_message(message.from_user.id, "/random")
        bot.send_message(message.from_user.id, "/search [your text]")
        bot.send_message(message.from_user.id,
                         "/search_genre_top [детектив/комедия/пародия/мехи/повседневность/романтика,/фантастика/этти]")
        bot.send_message(message.from_user.id, "/subscribe")
        bot.send_message(message.from_user.id, "/unsubscribe")
    elif len(commands) == 2 and commands[0] == "/top":
        if commands[1] == "random":
            res = parse.parse_top(100)
            answ = res[random.randrange(100)]
            bot.send_photo(message.from_user.id, answ[0], answ[1] + ": " + answ[2])
        else:
            res = parse.parse_top(int(commands[1]))
            for top_anim in res:
                bot.send_photo(message.from_user.id, top_anim[0], top_anim[1] + ": " + top_anim[2])
    elif commands[0] == "/new":
        res = parse.parse_new(5)
        for new in res:
            bot.send_photo(message.from_user.id, new[0], new[1] + ": " + new[2])
    elif commands[0] == "/random":
        res = parse.parse_random()
        bot.send_photo(message.from_user.id, res[0], res[1] + ": " + res[2])
    elif len(commands) >= 2 and commands[0] == "/search":
        ser = ""
        for word in range(1, len(commands)):
            ser = ser + commands[word] + "_"
        res = parse.search(ser)
        if res == []:
            bot.send_message(message.from_user.id, "Nothing was found.")
        else:
            for anim in res:
                bot.send_photo(message.from_user.id, anim[0], anim[1] + ": " + anim[2])
    elif len(commands) >= 2 and commands[0] == "/search_genre_top":
        index = parse.get_index(commands[1])
        if not index:
            bot.send_message(message.from_user.id, "Invalid genre.")
        else:
            res = parse.search_genre_top(index)
            for i in res:
                bot.send_photo(message.from_user.id, i[0], i[1] + ": " + i[2])
    elif commands[0] == "/subscribe":
        database.subscribe(message)
        print(message.from_user.id)
        bot.send_message(message.from_user.id, "You were subscribed.")
    elif commands[0] == "/unsubscribe":
        database.unsubscribe(message)
        bot.send_message(message.from_user.id, "You were unsubscribed.")
    elif commands[0] == "//send" and const.ADMIN:
        ser = ""
        for word in range(1, len(commands)):
            ser = ser + commands[word] + " "
        for sub in database.get_all_subs():
            bot.send_message(sub[0], ser)
    else:
        bot.send_message(message.from_user.id, "Invalid Command. Type /help for all commands.")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
