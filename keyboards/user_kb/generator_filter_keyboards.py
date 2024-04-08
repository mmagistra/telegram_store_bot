from create_bot import db_worker
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


def generate_filters_choose_inline_kb(filter_on_adjustment, exists_filters):
    request_filter = ''
    for key, values in exists_filters.items():
        request_filter += f'('
        if type(values) == list:
            for value in values:
                request_filter += f'{key}="{value}" OR '
        elif type(values) == str:
            request_filter += f'{values} IN description'
        elif type(values) == dict:
            price_max = values.get('price_max', 'not_found')
            price_min = values.get('price_min', 'not_found')
            if price_min != 'not_found':
                request_filter += f'{price_min} <= price'
                if price_max != 'not_found':
                    request_filter += f' AND price <= {price_max}'
            elif price_max != 'not_found':
                request_filter += f'price <= {price_max}'
        else:
            raise f'Unknown parameter {key} - {values}'
        try:
            request_filter = request_filter[:-4] + ') AND'
        except:
            request_filter = ''
    try:
        request_filter = request_filter[:-4]
    except:
        request_filter = ''

    all_variants = [i[0] for i in db_worker.products_read(
        request_filter=request_filter,
        select_filter=filter_on_adjustment)]
    possible_variants = list(set(all_variants))
    button_data = CallbackData(
        'filter_adjustment',
        'action',
        'filter_on_adjustment',
        'item')
    buttons = [InlineKeyboardButton(
        text=f'{"✅" if btn_name in exists_filters else ""}{btn_name} - {all_variants.count(btn_name)}',
        callback_data=button_data.new(action='remove' if btn_name in exists_filters else 'add',
                                      filter_on_adjustment=filter_on_adjustment,
                                      item=btn_name)) for btn_name in possible_variants]
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    accept_btn = InlineKeyboardButton(
        text='Подтвердить',
        callback_data=button_data.new(action='accept',
                                      filter_on_adjustment=filter_on_adjustment,
                                      item='accept')
    )
    keyboard.row(accept_btn)
    return keyboard
