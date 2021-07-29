import sqlite3


def subscribe(user_id, db):
    """
    Ставит параметр подписки данного пользователя на активен
    :param user_id: id пользователя
    :param db: название базы данных
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(userid INT PRIMARY KEY,sub INT);")
        if sub_exist(user_id, db):
            cur.execute("UPDATE users SET sub = 1 WHERE userid = {}".format(user_id))
        else:
            cur.execute("INSERT INTO users (userid, sub) VALUES ({}, {});".format(user_id, 1))
        conn.commit()


def unsubscribe(user_id, db):
    """
    Ставит параметр подписки данного пользователя на неактивен
    :param user_id: id пользователя
    :param db: название базы данных
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(userid INT PRIMARY KEY,sub INT);")
        if sub_exist(user_id, db):
            cur.execute("UPDATE users SET sub = 0 WHERE userid = {}".format(user_id))
        else:
            cur.execute("INSERT INTO users (userid, sub) VALUES ({}, {});".format(user_id, 0))
        conn.commit()


def get_all_subs(db):
    """
    Возвращает всех пользователей с активной подпиской
    :param db: название базы данных
    :return: id всех пользователей с активной подпиской
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        res = cur.execute("SELECT * FROM users WHERE sub = 1")
        return res.fetchall()


def sub_exist(user_id, db):
    """
    Определяет находится ли такой пользователь в базе  данных
    :param user_id: id пользователя
    :param db: название базы данных
    :return: находится пользователь в базе или нет
    """
    with sqlite3.connect(db) as conn:
        cur = conn.cursor()
        return bool(len(cur.execute("SELECT * FROM users WHERE userid = {}".format(user_id)).fetchall()))
