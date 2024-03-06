from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from aiogram.dispatcher import FSMContext
from keyboards import kb, ik
from utils.db_api import database as db
from data import config as cfg
from handlers.users import misc as ms


@dp.message_handler(CommandStart(), chat_type=types.ChatType.PRIVATE)
async def bot_start(message: types.Message, state:FSMContext):

	db.create_user(message.from_user.id,message.from_user.username)
	sub_status = await ms.check_subscribes(message.from_user.id)
	
	if sub_status == False:
		return await message.answer("Подпишитесь на каналы ниже, чтобы продолжать использовать Chat GPT.\n"
			"<b>Благодаря этому бот остаётся полностью бесплатным!</b>",reply_markup=ik.adv_chats())
        

	image = cfg.image
	await message.answer_photo(photo=image,caption=f"Привет, <b>{message.from_user.full_name}!</b>\n"
		f"Я бесплатный <b>Chat-GPT бот</b>, работающий на последней версии нейросети Open AI.",reply_markup=kb.main)