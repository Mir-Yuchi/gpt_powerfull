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
#chat
def insert_new_message(user_id, role, content):
    cur.execute("INSERT INTO chat VALUES(?,?,?)",(user_id,role,content))
    conn.commit()
def clear_chat(user_id):
    cur.execute("DELETE FROM chat WHERE user_id = ?",(user_id,))
    conn.commit()
def get_chat(user_id):
    datas = cur.execute("SELECT * FROM chat WHERE user_id = ?",(user_id,))
    s = []
    for data in datas:
        s.append({'role':data[1],'content':data[2]})
    return s
#Users
def create_user(userId,username):
    try:
        date = str(datetime.datetime.now())[:19]
        cur.execute("INSERT INTO users VALUES(?,?,?)",(userId,username,date))
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
        data = cur.execute("SELECT * FROM users WHERE id = ?",(userId,)).fetchone()
        return parse_user_data(data)
    except:
        pass

def update_userfield(user_id,field,update):
    cur.execute(f"UPDATE users SET {field} = ? WHERE id = ?",(update,user_id))
    conn.commit()

def plus_userfield(user_id,field,plus_value):
    old = cur.execute(f"SELECT {field} FROM users WHERE id = ?", (user_id,)).fetchone()[0]
    if old == None:
        old = ""
    new = old + plus_value
    update_userfield(user_id,field,new)