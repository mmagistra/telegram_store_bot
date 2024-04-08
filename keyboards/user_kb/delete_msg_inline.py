from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

# not used yet
delete_msg_inline_kb = InlineKeyboardMarkup()
delete_me_btn = InlineKeyboardButton(text='Удалить это сообщение', callback_data=f'delete_msg')
delete_msg_inline_kb.add(delete_me_btn)
