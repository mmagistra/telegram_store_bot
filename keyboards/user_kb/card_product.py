from create_bot import db_worker
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


def generate_card_product_kb(need_more_btn, product_id):
    card_product_kb = InlineKeyboardMarkup(row_width=1)
    pay_callback = CallbackData('pay', 'id')
    search_callback = CallbackData('search_cards')

    pay_btn = InlineKeyboardButton('Оплатить', callback_data=pay_callback.new(id=product_id))
    if need_more_btn:
        more_btn = InlineKeyboardButton('Показать еще...', callback_data=search_callback.new())
        card_product_kb.add(pay_btn, more_btn)
    else:
        card_product_kb.add(pay_btn)

    return card_product_kb
