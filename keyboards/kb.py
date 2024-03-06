from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

main = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1).add(
    KeyboardButton("💬 Начать общаться"),
    KeyboardButton("👻 Сгенерировать картинку"),
    KeyboardButton("😈 Наши проекты"),
)
chat = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1).add(
    KeyboardButton("🔁Сбросить контекст"),
    KeyboardButton("◀️Назад")
)
image_generate = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1).add(
    KeyboardButton("◀️Назад")
)
admin = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add(
    KeyboardButton("💬Рассылка"),
    KeyboardButton("📊Статистика"),
    KeyboardButton("🔃Выгрузить дб"),
    KeyboardButton("👥Управление каналами"),
    KeyboardButton("🗑Удалить мертвых пользователей"),
    KeyboardButton("📄Мои проекты")
)