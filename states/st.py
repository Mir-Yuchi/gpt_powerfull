import os

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from handlers.users import misc as ms
from utils.db_api import database as db
from data import config as cfg
from keyboards import ik, kb
from loader import bot
from utils import GPT as gpt


class UserState(StatesGroup):
    name = State()
    chat = State()
    draw = State()
    sender = State()
    add_btn_url = State()
    add_btn_name = State()
    midjourney = State()
    delete_users = State()


class Add_Channel(StatesGroup):
    c_id = State()
    c_name = State()
    c_url = State()


class Add_projects(StatesGroup):
    c_name = State()
    c_url = State()


@dp.message_handler(state=Add_projects.c_url)
async def main(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data(url=url)
    await message.answer("Введите надпись на кнопке")
    await Add_projects.c_name.set()


@dp.message_handler(state=Add_projects.c_name)
async def main(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    data = await state.get_data()
    db.create_projects(data['url'], name)
    await state.finish()
    await message.answer("✅Добавлен")


@dp.message_handler(commands=['close'], state="*")
async def close(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("❌Чат закрыт, память Chat GPT очищена.")


@dp.message_handler(state=UserState.chat)
async def main(message: types.Message, state: FSMContext):
    action = await dispatcher_buttons(message, state)
    if action == 1:
        return

    old_chat_history = db.get_chat(message.from_user.id)
    sub_status = await ms.check_subscribes(message.from_user.id)

    if sub_status == False and len(old_chat_history) != 0:
        await message.answer("Подпишитесь на каналы ниже, чтобы продолжать использовать Chat GPT.\n"
                             "<b>Благодаря этому бот остаётся полностью бесплатным!</b>", reply_markup=ik.adv_chats())
        return

    await state.finish()
    msg = await message.answer("⏳")
    promt = message.text.replace("\"", "")
    answer = await ms.get_gpt_answer(message.from_user.id, promt, old_chat_history, 0)
    await msg.delete()
    await msg.answer(answer)
    await UserState.chat.set()


@dp.message_handler(state=UserState.draw)
async def main(message: types.Message, state: FSMContext):
    action = await dispatcher_buttons(message, state)
    if action == 1:
        return

    await state.finish()
    msg = await message.answer("🎨")
    try:
        answer = await gpt.davinci(message.text, ms.get_random_token(), 1024)
    except:
        await msg.delete()
        await message.answer("😔Извините, я не смог обработать ваш запрос. Попробуйте спросить что-нибудь еще!")
        await UserState.draw.set()
        return
    await msg.delete()
    await msg.answer_photo(photo=answer)
    await UserState.draw.set()


async def dispatcher_buttons(message: types.Message, state: FSMContext):
    if message.text == "🔁Сбросить контекст":
        db.clear_chat(message.from_user.id)
        await message.answer("✅Контекст переписки с ботом сброшен")
        return 1
    elif message.text == "◀️Назад":
        image = cfg.image
        await message.answer_photo(photo=image, caption=f"👻 Главное меню",
                                   reply_markup=kb.main)
        await state.finish()
        return 1
    else:
        return 0


@dp.message_handler(state=UserState.sender, content_types=types.ContentType.ANY)
async def main(message: types.Message, state: FSMContext):
    msg_id = message.message_id
    await bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                           message_id=msg_id)
    await message.answer("Рассылаем?", reply_markup=ik.send(msg_id))
    await state.finish()


@dp.message_handler(state=UserState.add_btn_url)
async def main(message: types.Message, state: FSMContext):
    url = message.text
    await state.update_data(url=url)
    await message.answer("Введите надпись на кнопке")
    await UserState.add_btn_name.set()


@dp.message_handler(state=UserState.add_btn_name)
async def main(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    data = await state.get_data()
    mrkp = ik.create_sender_mrkp(name, data['url'])
    message_to_send = await bot.copy_message(chat_id=message.from_user.id, from_chat_id=message.from_user.id,
                                             message_id=data['message_id'], reply_markup=mrkp)
    await message.answer('Рассылаем?', reply_markup=ik.send(message_to_send.message_id))


@dp.message_handler(state=Add_Channel.c_id)
async def main(message: types.Message, state: FSMContext):
    try:
        await state.update_data(id=int(message.text))
        await message.answer("Введите имя канала", reply_markup=ik.off_state)
        await Add_Channel.c_name.set()
    except:
        await message.answer("❌Введите число", reply_markup=ik.off_state)


@dp.message_handler(state=Add_Channel.c_name)
async def main(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ссылку на вступление", reply_markup=ik.off_state)
    await Add_Channel.c_url.set()


@dp.message_handler(state=Add_Channel.c_url)
async def main(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()

    url = message.text
    db.create_adv_chat(data['id'], url, data['name'])
    await message.answer("✅Ваш канал успешно создан")


@dp.message_handler(state=UserState.delete_users, content_types=types.ContentType.DOCUMENT)
async def main(message: types.Message, state: FSMContext):
    await state.finish()
    file_path = (await message.document.get_file())['file_path']
    await message.document.download()
    file = open(file_path, 'r')
    msg = await message.answer("⏳")
    s = list(map(int, (file.read().split("\n"))[0:-1]))
    await msg.delete()
    file.close()
    db.delete_users_for_ids(s)
    os.remove(file_path)
    await message.answer("✅Мертвые пользователи удалены")
