import database
import os
import unittest
from main import generate_message


class Test(unittest.TestCase):
    test_cases_gen = [
        ("/help", 1),
        ("/something", 1),
        ("/top 1", 1),
        ("/top eioper", 1),
        ("/search нагаторо", 1),
        ("/search hgjfghj", 1),
        ("/search_genre_top этти", 1),
        ("/search_genre_top jfklj", 1)
    ]
    test_right_gen = [
        [(1, 'https://www.spletnik.ru/img/__post/66/66e7863b682b8d02f539a3f7d5b7f471_806.jpg',
          '/top random\n/top [number]\n/new\n/random\n/search [your text]\n/search_genre_top [детектив/комедия/пародия/мехи/повседневность/романтика,/фантастика/этти]\n/subscribe\n/unsubscribe\n',
          1)],
        [(1, 'https://znaiwifi.com/wp-content/uploads/2018/01/hqdefault.jpg',
          'Invalid Command. Type /help for all commands.', 1)],
        [(1, 'https://yummyanime.club//img/posters/1613122367.jpg',
          'Код Гиасс: Восстание Лелуша R2: https://yummyanime.club//catalog/item/kod-gias-vosstavshij-lelush-r2', 1)],
        [(1, 'https://znaiwifi.com/wp-content/uploads/2018/01/hqdefault.jpg',
          'Invalid Command. Type /help for all commands.', 1)],
        [(1, 'https://yummyanime.club//img/posters/1597596053.jpg',
          'Не издевайся, Нагаторо: https://yummyanime.club/catalog/item/ne-izdevajsya-nagatoro', 1)],
        [(1, 'https://znaiwifi.com/wp-content/uploads/2018/01/hqdefault.jpg', 'Nothing was found.', 1)],
        [(1, 'https://yummyanime.club//img/posters/1617200003.jpg',
          'Реинкарнация безработного: История о приключениях в другом мире: https://yummyanime.club/catalog/item/reinkarnaciya-bezrabotnogo-istoriya-o-priklyucheniyah-v-drugom-mire',
          5), (1, 'https://yummyanime.club//img/posters/1596925918.jpg',
               'Нет игры - нет жизни: Начало: https://yummyanime.club/catalog/item/net-igry-net-zhizni-s-nulya', 5), (
             1, 'https://yummyanime.club//img/posters/1570883985.jpg',
             'Кулинарные поединки Сомы: https://yummyanime.club/catalog/item/kulinarnye-poedinki-somy', 5), (
             1, 'https://yummyanime.club//img/posters/1578821002.jpg',
             'Кулинарные поединки Сомы: Второе блюдо: https://yummyanime.club/catalog/item/kulinarnye-poedinki-somy-tv-2',
             5), (1, 'https://yummyanime.club//img/posters/1595875111.jpg',
                  'Нет игры - нет жизни: https://yummyanime.club/catalog/item/igra-na-vyzhivanie', 5)],
        [(1, 'https://znaiwifi.com/wp-content/uploads/2018/01/hqdefault.jpg', 'Invalid genre.', 1)]
    ]
    test_bd_name = "test.bd"

    def test_gen(self):
        self.assertEqual(generate_message(*self.test_cases_gen[0]), self.test_right_gen[0])
        self.assertEqual(generate_message(*self.test_cases_gen[1]), self.test_right_gen[1])
        self.assertEqual(generate_message(*self.test_cases_gen[2]), self.test_right_gen[2])
        self.assertEqual(generate_message(*self.test_cases_gen[3]), self.test_right_gen[3])
        self.assertEqual(generate_message(*self.test_cases_gen[4]), self.test_right_gen[4])
        self.assertEqual(generate_message(*self.test_cases_gen[5]), self.test_right_gen[5])
        self.assertEqual(generate_message(*self.test_cases_gen[6]), self.test_right_gen[6])
        self.assertEqual(generate_message(*self.test_cases_gen[7]), self.test_right_gen[7])

    def test_db(self):
        if os.path.exists("test.bd"):
            os.remove("test.bd")
        database.subscribe(1, self.test_bd_name)
        self.assertEqual(database.get_all_subs(self.test_bd_name), [(1, 1)])
        self.assertEqual(database.sub_exist(1, self.test_bd_name), True)
        self.assertEqual(database.sub_exist(2, self.test_bd_name), False)
        database.subscribe(2, self.test_bd_name)
        self.assertEqual(database.get_all_subs(self.test_bd_name), [(1, 1), (2, 1)])
        database.unsubscribe(1, self.test_bd_name)
        self.assertEqual(database.get_all_subs(self.test_bd_name), [(2, 1)])
        self.assertEqual(database.sub_exist(1, self.test_bd_name), True)


if __name__ == "__main__":
    unittest.main()
