import random

import telebot as tb

import const
import database
import parse

bot = tb.TeleBot("Your TOKEN")


@bot.message_handler(commands=["start", "help"])
def send_start_or_help(message):
    """
    Получает сообщение с запросом помощи и отправляет ответ
    :param message: сообщение
    """
    res = get_help(message.from_user.id)
    bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(commands=["new"])
def send_new(message):
    """
    Получает сообщение с обновлениями аниме и отпровляет ответ
    :param message: сообщение
    """
    res = get_new(message.from_user.id)
    for messages in range(res[0][3]):
        bot.send_photo(res[messages][0], res[messages][1], res[messages][2])


@bot.message_handler(commands=["subscribe"])
def send_subscribe(message):
    """
    Получает запрос на подписку, подписывает и отправляет ответ
    :param message: сообщение
    """
    res = get_subscribe(message.from_user.id)
    bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(commands=["unsubscribe"])
def send_unsubscribe(message):
    """
    Получает запрос на отписку, отписывает и отправляет ответ
    :param message: сообщение
    """
    res = get_unsubscribe(message.from_user.id)
    bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(commands=["send"])
def send_unsubscribe(message):
    """
    Получает сообщение с запросом на отправку рассылики и отправлыет ее подписчикам
    :param message: сообщение
    """
    res = get_send(message.text, message.from_user.id)
    bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(commands=["top"])
def send_top(message):
    """
    Получает запрос топ с параметром и отправляет ответ
    :param message: сообщение
    """
    res = get_top(message.text, message.from_user.id)
    if isinstance(res[0], tuple):
        for messages in range(res[0][3]):
            bot.send_photo(res[messages][0], res[messages][1], res[messages][2])
    else:
        bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(commands=["random"])
def send_random(message):
    """
    Получает запрос на случайное аниме и отправляет ответ
    :param message: сообщение
    """
    res = get_random(message.from_user.id)
    bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(commands=["search"])
def send_search(message):
    """
    Получает сообщение с топ 5 по запросу и отправляет ответ
    :param message: сообщение
    """
    res = get_search(message.text, message.from_user.id)
    if isinstance(res[0], tuple):
        for messages in range(res[0][3]):
            bot.send_photo(res[messages][0], res[messages][1], res[messages][2])
    else:
        bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(commands=["search_genre_top"])
def send_search_genre(message):
    """
    Получает сообщение с топ 5 по жанру и отправляет ответ
    :param message: сообщение
    """
    res = get_search_genre(message.text, message.from_user.id)
    if isinstance(res[0], tuple):
        for messages in range(res[0][3]):
            bot.send_photo(res[messages][0], res[messages][1], res[messages][2])
    else:
        bot.send_photo(res[0], res[1], res[2])


@bot.message_handler(content_types=['text'])
def get_message(message):
    """
    Получает неверное сообщение и отправяет ответ
    :param message: сообщение
    """
    res = wrong_input(message.from_user.id)
    bot.send_photo(res[0], res[1], res[2])


def get_new(user_id):
    """
    Генерирует сообщение с обновлениями аниме
    :param user_id: ид пользователя
    :return: сообщение с обновлениями аниме
    """
    res = parse.parse_new(const.AMOUNT)
    return append_all(res, user_id)


def get_help(user_id):
    """
    Генерирует сообщение с помощью
    :param user_id: ид пользоваетля
    :return: сообщение с помощью
    """
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


def get_subscribe(user_id):
    """
    Подписывате пользователя
    :param user_id: ид пользователя
    :return: сообщение о подписке
    """
    database.subscribe(user_id, const.DATABASE)
    print(user_id)
    return user_id, const.SUB, "You were subscribed.", 1


def get_unsubscribe(user_id):
    """
    Отписывает польззователя
    :param user_id: ид пользователя
    :return: сообщение об отписке
    """
    database.unsubscribe(user_id, const.DATABASE)
    return user_id, const.UNSUB, "You were unsubscribed.", 1


def get_send(message_text, user_id):
    """
    Отправляет сообщение всем подписанным пользователям
    :param message_text: текст сообщения пользователя
    :param user_id: ид польззователя
    :return: лист из сообщения для всех подписчиков
    """
    commands = message_text.split()
    if const.ADMIN == user_id:
        return send(commands)
    return user_id, const.NOTHING, "Invalid Command. Type /help for all commands.", 1


def get_top(message_text, user_id):
    """
    Ищет аниме в топе
    :param message_text: текст сообщения пользователя
    :param user_id: ид польззователя
    :return: топ n аниме или случчайное аниме из топ 100
    """
    commands = message_text.split()
    if len(commands) == 2:
        return top(commands, user_id)
    return user_id, const.NOTHING, "Invalid Command. Type /help for all commands.", 1


def get_random(user_id):
    """
    Получает случайное аниме
    :param user_id: ид польззователя
    :return: случайное аниме
    """
    res = parse.parse_random()
    return user_id, res[0], res[1] + ": " + res[2], 1


def get_search(message_text, user_id):
    """
    Ищет аниме
    :param message_text: текст сообщения пользователя
    :param user_id: ид польззователя
    :return: топ 5 аниме по запросу
    """
    commands = message_text.split()
    if len(commands) >= 2:
        return search(commands, user_id)


def get_search_genre(message_text, user_id):
    """
    Ищет аниме по жанрам
    :param message_text: текст сообщения пользователя
    :param user_id: ид польззователя
    :return: топ 5 аниме указзанного жанра
    """
    commands = message_text.split()
    if len(commands) >= 2:
        return search_genre_top(commands, user_id)


def wrong_input(user_id):
    """
    Обрабатывает неправильные команды
    :param user_id: id пользователя
    :return: сообщение о неправильной команде
    """
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
