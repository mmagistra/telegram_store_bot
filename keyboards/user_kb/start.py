from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


start_kb = ReplyKeyboardMarkup(resize_keyboard=True)

b1 = KeyboardButton('/каталог')
b2 = KeyboardButton('/панель_администратора')
b3 = KeyboardButton('/о_нас')

start_kb.row(b1, b2).row(b3)
