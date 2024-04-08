from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


local_store_inline_kb = InlineKeyboardMarkup()

filter_adjustment_callback = CallbackData('filter_adjustment', 'action', 'filter_on_adjustment')
price_adjustment_callback = CallbackData('price_adjustment')
search_request_adjustment_callback = CallbackData('search_request_adjustment')
search_callback = CallbackData('search_cards')
cancel_callback = CallbackData('cancel')

gender_btn = InlineKeyboardButton(text='Добавить пол',
                                  callback_data=filter_adjustment_callback.new(action='start',
                                                                               # filter_on_adjustment - как название столбца в таблице,
                                                                               filter_on_adjustment='gender'))
type_btn = InlineKeyboardButton(text='Добавить тип одежды',
                                callback_data=filter_adjustment_callback.new(action='start',
                                # filter_on_adjustment - как название столбца в таблице,
                                filter_on_adjustment='type'))
size_btn = InlineKeyboardButton(text='Добавить размер',
                                callback_data=filter_adjustment_callback.new(action='start',
                                                                             # filter_on_adjustment - как название столбца в таблице,
                                                                             filter_on_adjustment='size'))
style_btn = InlineKeyboardButton(text='Добавить стиль',
                                 callback_data=filter_adjustment_callback.new(action='start',
                                                                              # filter_on_adjustment - как название столбца в таблице,
                                                                              filter_on_adjustment='style'))
seasonality_btn = InlineKeyboardButton(text='Добавить сезон',
                                       callback_data=filter_adjustment_callback.new(action='start',
                                                                                    # filter_on_adjustment - как название столбца в таблице,
                                                                                    filter_on_adjustment='seasonality'))
brand_btn = InlineKeyboardButton(text='Добавить бренд',
                                 callback_data=filter_adjustment_callback.new(action='start',
                                                                              # filter_on_adjustment - как название столбца в таблице,
                                                                              filter_on_adjustment='brand'))
price_btn = InlineKeyboardButton(text='Добавить цену',
                                 callback_data=price_adjustment_callback.new())
search_request_btn = InlineKeyboardButton(text='Добавить поисковой запрос',
                                          callback_data=search_request_adjustment_callback.new())
cancel_btn = InlineKeyboardButton(text='Отмена',
                                  callback_data=cancel_callback.new())
search_btn = InlineKeyboardButton(text='Поиск',
                                  callback_data=search_callback.new())

(local_store_inline_kb.row(
    gender_btn).row(
    type_btn).row(
    size_btn).row(
    style_btn).row(
    seasonality_btn).row(
    brand_btn).row(
    price_btn).row(
    search_request_btn).row(
    cancel_btn, search_btn))
