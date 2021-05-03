import sqlite3

admin_id = 470008567


def subscribe(message):
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(userid INT PRIMARY KEY,sub INT);")
        if sub_exist(message):
            cur.execute("UPDATE users SET sub = 1 WHERE userid = {}".format(message.from_user.id))
        else:
            cur.execute("INSERT INTO users (userid, sub) VALUES ({}, {});".format(message.from_user.id, 1))
        conn.commit()


def unsubscribe(message):
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS users(userid INT PRIMARY KEY,sub INT);")
        if sub_exist(message):
            cur.execute("UPDATE users SET sub = 0 WHERE userid = {}".format(message.from_user.id))
        else:
            cur.execute("INSERT INTO users (userid, sub) VALUES ({}, {});".format(message.from_user.id, 0))
        conn.commit()


def get_all_subs():
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        res = cur.execute("SELECT * FROM users WHERE sub = 1")
        return res.fetchall()


def sub_exist(message):
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        return bool(len(cur.execute("SELECT * FROM users WHERE userid = {}".format(message.from_user.id)).fetchall()))


def get_admin(message):
    return message.from_user.id == admin_id
