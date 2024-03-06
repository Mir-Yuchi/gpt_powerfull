import asyncio

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

import keyboards.kb
from loader import dp,bot
from data import config as cfg

from handlers.sender_handlers import sender_keyboard as kb
from handlers.sender_handlers import sender_db as db


from utils.db_api import database as main_db

class Sender_states(StatesGroup):
    main = State()
    text = State()
    photo = State()
    video = State()


@dp.message_handler(state=Sender_states.main)
async def main(message : types.Message,state : FSMContext):
    params = message.text.split("-")
    match params[0]:
        case "Текст":
            await message.answer("Введите текст, который будет прикреплен к рассылке\n"
                                 "Чтобы сделать текст жирным: *жирный*\n"
                                 "Чтобы сделать текст копируемым: `копируемый текст`",reply_markup=kb.back_mrkp)
            await Sender_states.text.set()
        case "Фото":
            if db.get_sender_data()['video_id'] != None:
                db.set_photoId(None)
                await message.answer('Вы уже прикрепили видео к рассылке. Оно было удалено из рассылки, т.к. '
                                     'бот не может отправить видео и фото одним сообщением.')
            await message.answer("Отправьте одно фото, которое будет прикрепленно к рассылке",reply_markup=kb.back_mrkp)
            await Sender_states.photo.set()
        case "Видео":
            if db.get_sender_data()['photo_id'] != None:
                db.set_photoId(None)
                await message.answer('Вы уже прикрепили фото к рассылке. Оно было удалено из рассылки, т.к. '
                                     'бот не может отправить видео и фото одним сообщением.')
            await message.answer("Отправьте одно видео, которое будет прикрепленно к рассылке",reply_markup=kb.back_mrkp)
            await Sender_states.video.set()
        case "Сбросить рассылку":
            db.refresh_db()
            await message.answer("Рассылка была сброшена")
        case "Разослать":
            await send(message)
        case "Предпросмотр":
            await message.answer("Предпросмотр:")
            await send_only_to_me(message)
        case "Назад":
            await state.finish()
            await message.answer("Основное меню админа:", reply_markup=keyboards.kb.admin)



@dp.message_handler(state=Sender_states.text)
async def main(message : types.Message,state : FSMContext):
    text = message.text
    db.set_text(text)
    await message.answer("Ваш текст установлен в рассылку")
    await Sender_states.main.set()

@dp.message_handler(state=Sender_states.photo,content_types=['photo'])
async def main(message : types.Message,state : FSMContext):
    photos = message.photo
    for photo in photos:
        photo_id = photo.file_id
        db.set_photoId(photo_id)
        break
    await message.answer("Ваше фото было добавлено в рассылку")
    await Sender_states.main.set()

@dp.message_handler(state=Sender_states.video,content_types=['video'])
async def main(message : types.Message,state : FSMContext):
    video_id = message.video.file_id
    db.set_videoId(video_id)
    await message.answer("Ваше видео было добавлено в рассылку")
    await Sender_states.main.set()

async def send(message: types.Message):
    ids = main_db.get_user_ids()
    photo_id = db.get_sender_data()['photo_id']
    video_id = db.get_sender_data()['video_id']
    text = db.get_sender_data()['text']
    await message.answer("Рассылка запущена.")
    if photo_id != None:
        k = 0
        for id in ids:
            try:
                await bot.send_photo(chat_id=id, photo=photo_id, caption=text, parse_mode="Markdown")
                await asyncio.sleep(0.2)
                k += 1
            except:
                pass
        await message.answer(f"Рассылка была отправлена {k} пользователям")
    elif video_id != None:
        k = 0
        for id in ids:
            try:
                await bot.send_video(chat_id=id, video=video_id, caption=text, parse_mode="Markdown")
                await asyncio.sleep(0.2)
                k += 1
            except:
                pass
        await message.answer(f"Рассылка была отправлена {k} пользователям")
    elif text != None:
        k = 0
        for id in ids:
            try:
                await bot.send_message(chat_id=id,text=text, parse_mode="Markdown")
                await asyncio.sleep(0.2)
                k += 1
            except:
                pass
        await message.answer(f"Рассылка была отправлена {k} пользователям")
    else:
        await message.answer("Ошибка! Рассылка не была отправлена")

async def send_only_to_me(message: types.Message):
    photo_id = db.get_sender_data()['photo_id']
    video_id = db.get_sender_data()['video_id']
    text = db.get_sender_data()['text']
    if photo_id != None:
        try:
            await bot.send_photo(chat_id=message.from_user.id, photo=photo_id, caption=text, parse_mode="Markdown")
        except:
            pass
    elif video_id != None:
        try:
            await bot.send_video(chat_id=message.from_user.id, video=video_id, caption=text, parse_mode="Markdown")
        except:
            pass
    elif text != None:
        try:
            await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode="Markdown")
        except:
            pass
    else:
        await message.answer("Ошибка! Рассылка не была отправлена")