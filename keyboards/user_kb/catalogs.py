from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


catalogs_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

b1 = KeyboardButton('/наш_магазин')
b2 = KeyboardButton('/wildberries')

catalogs_kb.row(b1, b2)
