from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

#клавиатура для работы с админами

b1 = KeyboardButton('/Добавить_администратора')
b2 = KeyboardButton('/Удалить_администратора')
b3 = KeyboardButton('/Просмотерть_список_администраторов')

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(b1).add(b2).add(b3)

