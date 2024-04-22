from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api import database as db

chatting = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="💬Начать общаться", callback_data='start_chatting')
)

off_state = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text="❌Отмена", callback_data='off_state')
)


def send(message_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="💬Разослать", callback_data=f'send-{message_id}'),
        InlineKeyboardButton(text="➕Добавить кнопку", callback_data=f'add_button_to_send-{message_id}'),
        InlineKeyboardButton(text="❌Отмена", callback_data='off_state')
    )


def create_sender_mrkp(name, url):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text=name, url=url)
    )


def adv_chats():
    mrkp = InlineKeyboardMarkup(row_width=1)
    datas = db.get_all_adv_chats()
    datas.reverse()
    for data in datas:
        mrkp.add(
            InlineKeyboardButton(text=data['name'], url=data['url'])
        )
    mrkp.add(
        InlineKeyboardButton(text="✅Я подписался", callback_data='im_subscribed')
    )
    return mrkp


def admin_adv_chats():
    datas = db.get_all_adv_chats()
    mrkp = InlineKeyboardMarkup(row_width=1)
    for data in datas:
        mrkp.add(
            InlineKeyboardButton(text=data['name'], callback_data=f'chat_manage-show-*{data["id"]}')
        )
    mrkp.add(
        InlineKeyboardButton(text="➕Добавить канал", callback_data='chat_manage-add_channel-*0')
    )
    return mrkp


def admin_delete_adv_chat(chat_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='🪣Удалить чат', callback_data=f'chat_manage-delete-*{chat_id}')
    )


use_new_bot = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text="😈Запустить😈", url="https://t.me/Pro_Midjourney_bot")
)


def projects():
    data = db.get_all_projects()
    mrkp = InlineKeyboardMarkup(row_width=1)
    for datas in data:
        mrkp.add(
            InlineKeyboardButton(text=datas['name'], url=datas['url'])
        )
    return mrkp


def admin_delete_projects(url):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text='🪣Удалить', callback_data=f'st-delete-*{url}')
    )


def admin_projects():
    data = db.get_all_projects()
    mrkp = InlineKeyboardMarkup(row_width=1)
    for datas in data:
        mrkp.add(
            InlineKeyboardButton(text=datas['name'], callback_data=f'st-parse_projects-*{datas["url"]}')
        )
    mrkp.add(
        InlineKeyboardButton(text="➕Добавить", callback_data='st-add_projects-*0')
    )
    return mrkp


def create_projects_mrkp(name, url):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text=name, url=url)
    )
