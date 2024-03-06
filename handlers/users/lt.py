from utils.db_api import database as db

def adv_chat_stat(chat_id):
    data = db.get_adv_chat(chat_id)
    return f"Канал: <b>{data['name']}</b>\n" \
           f"ID: <code>{data['id']}</code>\n\n" \
           f"Привидено пользователей: <b>{data['user_count']}</b>"


def adv_projects(url):
    data = db.get_adv_projects(url)
    return f"Проект: <b>{data['name']}</b>\n" \
           f"URL: <code>{data['url']}</code>\n\n"