import sqlite3
from data import config as cfg
from loader import bot
import datetime

conn = sqlite3.connect(r"utils\db_api\database.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    id PRIMARY KEY,
    username TEXT,
    date TEXT)
""")
cur.execute("""CREATE TABLE IF NOT EXISTS chat(
    user_id INT,
    role TEXT,
    content TEXT)
""")
cur.execute("""CREATE TABLE IF NOT EXISTS tokens(
    token TEXT PRIMARY KEY,
    error INT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS adv_chats(
    id INT PRIMARY KEY,
    user_count INT,
    url TEXT,
    name TEXT
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS projects(
    url TEXT,
    name TEXT
)""")


def create_projects(url, name):
    try:
        cur.execute("INSERT INTO projects VALUES(?,?)", (url, name))
        conn.commit()
    except:
        pass


def get_adv_projects(url):
    x = cur.execute("SELECT * FROM projects WHERE url = ?", (url,)).fetchone()
    return parse_projectsa(x)


def parse_projectsa(data):
    return {'url': data[0], 'name': data[1]}


def delete_adv_projects(url):
    cur.execute("DELETE FROM projects WHERE url = ?", (url,))
    conn.commit()


def get_all_projects():
    res = []
    datas = cur.execute("SELECT * FROM projects").fetchall()
    for data in datas:
        res.append(parse_projectsa(data))
    return res


# adv_chat
def create_adv_chat(id, url, name):
    try:
        cur.execute("INSERT INTO adv_chats VALUES(?,?,?,?)", (id, 0, url, name))
        conn.commit()
    except:
        pass


def get_adv_chat(id):
    x = cur.execute("SELECT * FROM adv_chats WHERE id = ?", (id,)).fetchone()
    return parse_adv_chat_data(x)


def get_all_adv_chats():
    res = []
    datas = cur.execute("SELECT * FROM adv_chats").fetchall()
    for data in datas:
        res.append(parse_adv_chat_data(data))
    return res


def get_all_adv_chats_id():
    res = []
    datas = cur.execute("SELECT * FROM adv_chats").fetchall()
    for data in datas:
        res.append(data[0])
    return res


def parse_adv_chat_data(data):
    return {'id': data[0], 'user_count': data[1], 'url': data[2], 'name': data[3]}


def delete_adv_chat(id):
    cur.execute("DELETE FROM adv_chats WHERE id = ?", (id,))
    conn.commit()


def update_adv_chat_field(chat_id, field, update):
    cur.execute(f"UPDATE adv_chats SET {field} = ? WHERE id = ?", (update, chat_id))
    conn.commit()


def plus_adv_chat_field(chat_id, field, plus_value):
    old = cur.execute(f"SELECT {field} FROM adv_chats WHERE id = ?", (chat_id,)).fetchone()[0]
    if old == None:
        old = ""
    new = old + plus_value
    update_adv_chat_field(chat_id, field, new)


def plus_user_count_to_all():
    ids = get_all_adv_chats_id()
    for id in ids:
        plus_adv_chat_field(id, 'user_count', 1)


# tokens
# def insert_tokens(tokens):
# insert = []
# for token in tokens:
# insert.append((token,0))
# cur.executemany("INSERT INTO tokens VALUES(?,?)",insert)
# conn.commit()
def get_errors(token):
    data = cur.execute("SELECT * FROM tokens WHERE token = ?", (token,)).fetchone()
    return data[1]


def plus_error(token):
    old = cur.execute(f"SELECT error FROM tokens WHERE token = ?", (token,)).fetchone()[0]
    if old == None:
        old = 0
    new = old + 1
    cur.execute("UPDATE tokens SET error = ? WHERE token = ?", (new, token))
    conn.commit()


def clear_token_database():
    cur.execute("DELETE FROM tokens")
    conn.commit()


def delete_token_if(token):
    errors = get_errors(token)
    need_to_delete = 100
    if errors >= need_to_delete:
        delete_token_from_file(token)


def delete_token_from_file(token):
    cfg.tokens.remove(token)
    tokens_file = open('tokens.txt', 'w')
    deleted_tokens_file = open("deleted_tokens.txt", 'a')

    text = ""
    for t in cfg.tokens:
        text += f"{t}\n"
    tokens_file.write(text)
    deleted_tokens_file.write(token + "\n")


# chat
def insert_new_message(user_id, role, content):
    cur.execute("INSERT INTO chat VALUES(?,?,?)", (user_id, role, content))
    conn.commit()


def clear_chat(user_id):
    cur.execute("DELETE FROM chat WHERE user_id = ?", (user_id,))
    conn.commit()


def get_chat(user_id):
    datas = cur.execute("SELECT * FROM chat WHERE user_id = ?", (user_id,))
    s = []
    for data in datas:
        s.append({'role': data[1], 'content': data[2]})
    return s


# Users
def create_user(userId, username):
    try:
        date = str(datetime.datetime.now())[:19]
        cur.execute("INSERT INTO users VALUES(?,?,?)", (userId, username, date))
        conn.commit()
    except Exception as e:
        pass


def get_user_ids():
    result = []
    cortejs = cur.execute("SELECT * FROM users")
    for crtj in cortejs:
        result.append(int(crtj[0]))
    return result


def get_all_users():
    result = []
    cortejs = cur.execute("SELECT * FROM users")
    for crtj in cortejs:
        result.append(parse_user_data(crtj))
    return result


def parse_user_data(data):
    return {'id': data[0], 'username': data[1], 'date': data[2]}


def get_user(userId):
    try:
        data = cur.execute("SELECT * FROM users WHERE id = ?", (userId,)).fetchone()
        return parse_user_data(data)
    except:
        pass


def update_userfield(user_id, field, update):
    cur.execute(f"UPDATE users SET {field} = ? WHERE id = ?", (update, user_id))
    conn.commit()


def plus_userfield(user_id, field, plus_value):
    old = cur.execute(f"SELECT {field} FROM users WHERE id = ?", (user_id,)).fetchone()[0]
    if old == None:
        old = ""
    new = old + plus_value
    update_userfield(user_id, field, new)


def delete_users_for_ids(ids: list):
    for id in ids:
        cur.execute(f"DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
