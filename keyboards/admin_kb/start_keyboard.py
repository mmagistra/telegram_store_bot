from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


#1 клавиатура для выбора действия
b1 = KeyboardButton('/Товар')
b2 = KeyboardButton('/Администраторы')

start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.row(b1, b2)

