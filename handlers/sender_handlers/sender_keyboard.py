from aiogram.types import KeyboardButton,ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

main_send_mrkp = ReplyKeyboardMarkup(resize_keyboard=True,row_width=3).add(
    KeyboardButton("Разослать")).add(KeyboardButton("Текст"),KeyboardButton("Фото"),KeyboardButton("Видео"),
    KeyboardButton("Сбросить рассылку"),KeyboardButton("Предпросмотр")).add(KeyboardButton("Назад")
)


back_mrkp = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Отменить ввод",callback_data="back_send-"))