from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api import database as db
from data.config import tokens
from handlers.users import misc as ms

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    db.clear_token_database()
    #db.insert_tokens(tokens)


if __name__ == '__main__':
    ms.delete_dublicates()
    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)

