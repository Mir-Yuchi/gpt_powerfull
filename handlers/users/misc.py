from data import config as cfg
from utils.db_api import database as db
from datetime import datetime
import random
from data.config import tokens
from loader import bot
import asyncio
from keyboards import ik
from utils import GPT as gpt


def admin_stat_text():
    users = db.get_all_users()
    u_lst = []
    for i in [1, 7, 30]:
        u_lst.append(get_count_of_user(i, users))
    text = "<b>Статистика</b>\n\n" \
           f"<b>Пользователей в боте:</b> {len(users)}\n" \
           f"<b>Пользователей за 1 день:</b> {u_lst[0]}\n" \
           f"<b>Пользователей за 7 дней:</b> {u_lst[1]}\n" \
           f"<b>Пользователей за 30 дней:</b> {u_lst[2]}\n\n"
    return text


def get_count_of_user(days, user_datas):
    counter = 0
    for data in user_datas:
        date = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - date).days < days:
            counter += 1
    return counter


async def get_gpt_answer(user_id, promt, old, i):
    print("Вопрос задался")
    if i >= 5:
        print(f"{user_id} Не получил ответ")
        db.clear_chat(user_id)
        return "Chat GPT не может ответить на этот вопрос.\n" \
               "Память была сброшена. Задайте свой вопрос ещё раз"
    token = get_random_token()
    try:
        answer = await gpt.ask(promt, token, old)
        if answer == 0:
            print(f"{user_id} Попытка #{i}")
            return (await get_gpt_answer(user_id, promt, old, i + 1))
        db.insert_new_message(user_id, 'user', promt)
        db.insert_new_message(user_id, 'assistant', answer)
        return answer
    except Exception as e:
        print(e)
        db.clear_chat(user_id)
        db.plus_error(token)
        db.delete_token_if(token)
        return "😔Извините, я не смог обработать ваш запрос. Попробуйте спросить что-нибудь еще!"


def get_random_token():
    print(len(tokens))
    rnd = random.randint(0, len(tokens) - 1)
    return tokens[rnd]


def get_ids_files():
    ids = db.get_user_ids()
    text = ""
    file = open("db_ids.txt", 'w')
    for id in ids:
        text += f"{id}\n"
    file.write(text)
    file.close()
    return open("db_ids.txt", 'rb')


async def sender(message_id, from_chat_id, name, url):
    if name == "0" or url == "0":
        ids = db.get_user_ids()
        i = 0
        for user_id in ids:
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id,
                                       message_id=message_id)
                i += 1
            except:
                pass
            await asyncio.sleep(0.2)
        await bot.send_message(chat_id=from_chat_id, text=f"Рассылка дошла до {i} пользователей")
    else:
        ids = db.get_user_ids()
        i = 0
        for user_id in ids:
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=from_chat_id,
                                       message_id=message_id, reply_markup=ik.create_sender_mrkp(name, url))
                i += 1
            except:
                pass
            await asyncio.sleep(0.2)
        await bot.send_message(chat_id=from_chat_id, text=f"Рассылка дошла до {i} пользователей")


async def check_subscribes(user_id):
    datas = db.get_all_adv_chats()
    for data in datas:
        if data['id'] > 0:
            continue
        user_channel_status = await bot.get_chat_member(chat_id=data['id'], user_id=user_id)
        if user_channel_status["status"] == 'left':
            return False
    db.plus_user_count_to_all()
    return True


def delete_dublicates():
    with open("tokens.txt", "r") as file:
        unique_lines = set(file.readlines())
    with open("tokens.txt", "w") as file:
        file.writelines(unique_lines)
