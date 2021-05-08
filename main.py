import random

import telebot as tb

import const
import database
import parse

bot = tb.TeleBot(const.TOKEN)


@bot.message_handler(content_types=['text'])
def get_message(message):
    """
    Получает сообщение и отправяет ответ
    :param message: сообщение
    """
    res = generate_message(message.text, message.from_user.id)
    for i in range(res[0][3]):
        bot.send_photo(res[i][0], res[i][1], res[i][2])


def generate_message(message_text, user_id):
    """
    Обрабатывает полученное сообщение и генерирует ответ
    :param message_text: текст сообщения
    :param user_id: id пользователя
    """
    commands = message_text.split()
    ans_to = []
    if commands[0] == "/help" or commands[0] == "/start":
        ans_to.append((user_id, const.HELP,
                       "/top random\n" +
                       "/top [number]\n" +
                       "/new\n" +
                       "/random\n" +
                       "/search [your text]\n" +
                       "/search_genre_top [детектив/комедия/пародия/мехи/повседневность/романтика,/фантастика/этти]\n" +
                       "/subscribe\n" +
                       "/unsubscribe\n", 1))
    if len(commands) == 2 and commands[0] == "/top":
        if commands[1] == "random":
            res = parse.parse_top(100)
            answ = res[random.randrange(100)]
            ans_to.append((user_id, answ[0], answ[1] + ": " + answ[2], 1))
        elif commands[1].isnumeric():
            res = parse.parse_top(int(commands[1]))
            for top_anim in res:
                ans_to.append((user_id, top_anim[0], top_anim[1] + ": " + top_anim[2], len(res)))
        else:
            ans_to.append((user_id, const.NOTHING, "Invalid Command. Type /help for all commands.", 1))
    if commands[0] == "/new":
        res = parse.parse_new(5)
        for new in res:
            ans_to.append((user_id, new[0], new[1] + ": " + new[2], len(res)))
    if commands[0] == "/random":
        res = parse.parse_random()
        ans_to.append((user_id, res[0], res[1] + ": " + res[2], 1))
    if len(commands) >= 2 and commands[0] == "/search":
        ser = ""
        for word in range(1, len(commands)):
            ser = ser + commands[word] + "_"
        res = parse.search(ser)
        if res == []:
            ans_to.append((user_id, const.NOTHING, "Nothing was found.", 1))
        else:
            for anim in res:
                ans_to.append((user_id, anim[0], anim[1] + ": " + anim[2], len(res)))
    if len(commands) >= 2 and commands[0] == "/search_genre_top":
        index = parse.get_index(commands[1])
        if index < 0:
            ans_to.append((user_id, const.NOTHING, "Invalid genre.", 1))
        else:
            res = parse.search_genre_top(index)
            for i in res:
                ans_to.append((user_id, i[0], i[1] + ": " + i[2], len(res)))
    if commands[0] == "/subscribe":
        database.subscribe(user_id, const.DATABASE)
        print(user_id)
        ans_to.append((user_id, const.SUB, "You were subscribed.", 1))
    if commands[0] == "/unsubscribe":
        database.unsubscribe(user_id, const.DATABASE)
        ans_to.append((user_id, const.UNSUB, "You were unsubscribed.", 1))
    if commands[0] == "//send" and const.ADMIN == user_id:
        ser = ""
        for word in range(1, len(commands)):
            ser = ser + commands[word] + " "
        for sub in database.get_all_subs(const.DATABASE):
            ans_to.append((sub[0], const.ALL, ser, len(database.get_all_subs(const.DATABASE))))
    if len(ans_to):
        ans_to.append((user_id, const.NOTHING, "Invalid Command. Type /help for all commands.", 1))
    return ans_to


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
