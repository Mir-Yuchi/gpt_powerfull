from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot
from data import config as cfg

from handlers.sender_handlers import sender_keyboard as kb
from handlers.sender_handlers import sender_states as st
from handlers.sender_handlers import sender_db as db


async def main(message: types.Message):
    db.refresh_db()
    await message.answer("Меню рассылки", reply_markup=kb.main_send_mrkp)
    await st.Sender_states.main.set()
