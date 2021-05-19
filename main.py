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
    if isinstance(res[0], tuple):
        for i in range(res[0][3]):
            bot.send_photo(res[i][0], res[i][1], res[i][2])
    else:
        bot.send_photo(res[0], res[1], res[2])


def generate_message(message_text, user_id):
    """
    Обрабатывает полученное сообщение и генерирует ответ
    :param message_text: текст сообщения
    :param user_id: id пользователя
    """
    commands = message_text.split()
    if commands[0] == "/help" or commands[0] == "/start":
        return user_id, const.HELP, \
               ("/top random - случайное аниме из топ100\n" +
                "/top [number] - топ number аниме с сайта\n" +
                "/new - обновления аниме на сайте(новые поступления и тд)\n" +
                "/random - случайное аниме с сайта\n" +
                "/search [your text] - поиск аниме по запросу your text\n" +
                "/search_genre_top [детектив/комедия/пародия/мехи/повседневность/романтика,/фантастика/этти]" +
                " - топ 5 аниме по жанру\n" +
                "/subscribe - подписаться на рассылку\n" +
                "/unsubscribe - отписаться от рассылки\n"), 1
    elif len(commands) == 2 and commands[0] == "/top":
        return top(commands, user_id)
    elif commands[0] == "/new":
        res = parse.parse_new(const.AMOUNT)
        return append_all(res, user_id)
    elif commands[0] == "/random":
        res = parse.parse_random()
        return user_id, res[0], res[1] + ": " + res[2], 1
    elif len(commands) >= 2 and commands[0] == "/search":
        return search(commands, user_id)
    elif len(commands) >= 2 and commands[0] == "/search_genre_top":
        return search_genre_top(commands, user_id)
    elif commands[0] == "/subscribe":
        database.subscribe(user_id, const.DATABASE)
        print(user_id)
        return user_id, const.SUB, "You were subscribed.", 1
    elif commands[0] == "/unsubscribe":
        database.unsubscribe(user_id, const.DATABASE)
        return user_id, const.UNSUB, "You were unsubscribed.", 1
    elif commands[0] == "//send" and const.ADMIN == user_id:
        return send(commands)
    else:
        return user_id, const.NOTHING, "Invalid Command. Type /help for all commands.", 1


def append_all(info_list, user_id):
    """
    Делает из листа, который возврощается функциями парс лист, который можно отправлять в функцию посылки
    :param info_list: лист, который вернула функция парс
    :param user_id: ид пользователя
    :return: упорядоченное сообщение
    """
    res = []
    for info in info_list:
        res.append((user_id, info[0], info[1] + ": " + info[2], len(info_list)))
    return res


def top(commands, user_id):
    """
    Обработка команды /top
    :param commands: полный набор аргументов
    :param user_id: ид пользователя
    :return: упорялоченное для вывода сообщение
    """
    if commands[1] == "random":
        res = parse.parse_top(100)
        answ = res[random.randrange(100)]
        return user_id, answ[0], answ[1] + ": " + answ[2], 1
    elif commands[1].isnumeric():
        res = parse.parse_top(int(commands[1]))
        return append_all(res, user_id)
    else:
        return user_id, const.NOTHING, "Invalid Command. Type /help for all commands.", 1


def search(commands, user_id):
    """
    Обработка команды /search
    :param commands: полный набор аргументов
    :param user_id: ид пользователя
    :return: упорялоченное для вывода сообщение
    """
    ser = "_".join(commands[1:])
    res = parse.search(ser)
    if not res:
        return user_id, const.NOTHING, "Nothing was found.", 1
    else:
        return append_all(res, user_id)


def search_genre_top(commands, user_id):
    """
    Обработка команды /search_genre_top
    :param commands: полный набор аргументов
    :param user_id: ид пользователя
    :return: упорялоченное для вывода сообщение
    """
    index = parse.get_index(commands[1])
    if index < 0:
        return user_id, const.NOTHING, "Invalid genre.", 1
    else:
        res = parse.search_genre_top(index)
        return append_all(res, user_id)


def send(commands):
    """
    Обрабатываает команду //send
    :param commands: полный список команд
    :return: упорялоченное для вывода сообщение
    """
    word = "_".join(commands[1:])
    ans_to = []
    for sub in database.get_all_subs(const.DATABASE):
        ans_to.append((sub[0], const.ALL, word, len(database.get_all_subs(const.DATABASE))))
    return ans_to


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
