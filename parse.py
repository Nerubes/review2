import cloudscraper
from bs4 import BeautifulSoup

import genre


def get_name(string, past):
    """
    Находит ссылку на объект в части html документа
    :param string: часть документа
    :param past: ожидаемая переменная, которой присвоена ссылка
    :return: ссылка
    """
    res = ""
    for i in range(len(past) + 1, len(string)):
        if string[i - len(past) - 2:i] == past + "=\"":
            while string[i] != "\"":
                res += string[i]
                i += 1
            break
    return res


def get_update(string):
    """
    Получает дату обновления, название тайтла и описание обновления
    :param string: откуда надо достать информацию
    :return: дату обновления, название тайтла и описание обновления
    """
    return str(string.find_all("span", class_="update-date"))[27:][:-8] + ". " + str(
        string.find_all("span", class_="update-title"))[28:][:-8] + ". " + str(
        string.find_all("span", class_="update-info"))[27:][:-8]


def get_index(genre_search):
    """
    Возвращает индекс жанра на сайте
    :param genre_search: жанр
    :return: индекс жанра
    """
    if genre_search in genre.search_index:
        return genre.search_index[genre_search]
    else:
        return -1


def parse_top(amount):
    """
    Парсит аниме из раздела топ 100 на сайте
    :param amount: количество
    :return: лист из листов состоящих из ссылок на изобраения, имен и ссылкок на сраницы
    """
    scraper = cloudscraper.create_scraper()
    site = "https://yummyanime.club/top"
    response = scraper.get(site)
    response.encoding = "utf8"
    text = response.text
    soup = BeautifulSoup(text, "lxml")
    hrefs = soup.find_all("a", class_="image-block")
    res = []
    index = 0
    for href in hrefs:
        if index >= amount:
            break
        i = ("https://yummyanime.club/" + get_name(str(href), "src"), get_name(str(href), "alt"),
             "https://yummyanime.club/" + get_name(str(href), "href"))
        res.append(i)
        index += 1
    response.connection.close()
    return res


def parse_new(amount):
    """
    Парсит аниме из новостей
    :param amount: количество
    :return: лист из листов состоящих из ссылок на изобраения, имен,
    описаний изменений, дат изменений и ссылкок на сраницы аниме
    """
    res = []
    while res == []:
        scraper = cloudscraper.create_scraper()
        site = "https://yummyanime.club/anime-updates"
        response = scraper.get(site)
        response.encoding = "utf8"
        text = response.text
        soup = BeautifulSoup(text, "lxml")
        hrefs = soup.find_all("a")
        index = 0
        for href in hrefs:
            if str(href).find("/img/poster") != -1:
                if index >= amount:
                    break
                i = ("https://yummyanime.club/" + get_name(str(href), "src"), get_update(href),
                     "https://yummyanime.club/" + get_name(str(href), "href"))
                res.append(i)
                index += 1
    response.connection.close()
    return res


def parse_random():
    """
    Делает запрос скрипту который выдает случайное аниме с сайте
    :return: лист состоящий из ссылки на картинку, наззвания и ссылки на страницу аниме
    """
    scraper = cloudscraper.create_scraper()
    site = "https://yummyanime.club/random"
    response = scraper.get(site)
    response.encoding = "utf8"
    text = response.text
    soup = BeautifulSoup(text, "lxml")
    img = soup.find_all("div", class_="poster-block")
    response.connection.close()
    return "https://yummyanime.club/" + get_name(str(img), "src"), get_name(
        str(soup.find_all("div", class_="rating-info")), "title"), response.url


def search(word):
    """
    Отправвляет запрос на страницу поиска аниме и возвращает первыее 5 результатотов
    :param word: слова поиска
    :return: лист из листов состоящих из ссылок на изобраения, имен и ссылкок на сраницы
    """
    scraper = cloudscraper.create_scraper()
    site = "https://yummyanime.club/get-search-list?&word=" + word + "&page=1"
    response = scraper.get(site)
    response.encoding = "utf8"
    res = []
    index = 0
    for anims in response.json()["animes"]["data"]:
        if index >= 5:
            break
        i = "https://yummyanime.club/" + str(anims["image"]), str(
            anims["name"]), "https://yummyanime.club/catalog/item/" + str(
            anims["alias"])
        res.append(i)
        index += 1
    response.connection.close()
    return res


def search_genre_top(index):
    """
    Отправвляет запрос на страницу поиска аниме по жанрам и возвращает первые 5 результатотов
    :param index: номер жанра
    :return: лист из листов состоящих из ссылок на изобраения, имен и ссылкок на сраницы
    """
    scraper = cloudscraper.create_scraper()
    site = "https://yummyanime.club/get-filter-list?&selected_category[]=" + str(
        index) + "&status=-1&season=0&selected_age=0&sort=3&sort_order=0&page=1"
    response = scraper.get(site)
    response.encoding = "utf8"
    res = []
    index = 0
    for anims in response.json()["animes"]["data"]:
        if index >= 5:
            break
        i = "https://yummyanime.club/" + str(anims["image"]), str(
            anims["name"]), "https://yummyanime.club/catalog/item/" + str(
            anims["alias"])
        res.append(i)
        index += 1
    response.connection.close()
    return res
