from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

#клавиатура для работы с товаром

b1 = KeyboardButton('/Добавить_товар')
b2 = KeyboardButton('/Удалить_товар')
b3 = KeyboardButton('/Изменить_информацию_о_товаре')
b4 = KeyboardButton('/Посмотреть_информацию_о_товаре')

product_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
product_keyboard.row(b1, b2).row(b3, b4)
