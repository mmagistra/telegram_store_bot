from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

b1 = 'name'
b2 = 'photo'
b3 = 'gender'
b4 = 'type_of_clothing'
b5 = 'size'
b6 = 'style'
b7 = 'seasonality'
b8 = 'brand'
b9 = 'price'
b10 = 'url'

kb = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
kb.row(b1, b2, b3).row(b4, b5, b6).row(b7, b8, b9, b10)
