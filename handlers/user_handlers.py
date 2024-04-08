from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import WrongFileIdentifier

from create_bot import db_worker
from keyboards.user_kb.test import test_kb
from keyboards.user_kb.start import start_kb
from keyboards.user_kb.filter import filter_keyboards
from keyboards.user_kb.local_store_inline import local_store_inline_kb
from keyboards.user_kb.generator_filter_keyboards import generate_filters_choose_inline_kb
from keyboards.user_kb.delete_msg_inline import delete_msg_inline_kb
from keyboards.user_kb.card_product import generate_card_product_kb
from keyboards.user_kb.catalogs import catalogs_kb


class SearcherFSM(StatesGroup):
    # locals
    # wait_for_local_filters_selected = State()  *not use yet
    wait_for_local_filter_adjustment = State()

    wait_for_local_min_price_adjustment = State()
    wait_for_local_max_price_adjustment = State()

    wait_for_search_request = State()

    # wildberries
    wait_for_wildberries_filter_adjustment = State()
    wait_for_wildberries_filters_selected = State()


async def start_cmd(message: Message, state: FSMContext):
    # проверка существования пользователя в БД и дальнейшее его добавление
    count_of_user_with_cur_id = len(db_worker.users_read(request_filter=f"user_id={message.from_user.id}"))
    if count_of_user_with_cur_id == 0:
        db_worker.users_add(message.from_user.id, message.from_user.full_name, 'user', True)
    elif count_of_user_with_cur_id != 1:
        raise f'2 user with same id ({message.from_user.id}) was found'
    # проверка актуальности данных пользователя и их изменения при необходимости
    old_user_fullname = db_worker.users_read(request_filter=f"user_id={message.from_user.id}",
                                             select_filter='user_name')[0]
    if old_user_fullname != message.from_user.full_name:
        db_worker.users_update(id=message.from_user.id, user_name=message.from_user.full_name)
    # начало работы с пользователем (стартовое сообщение, клавиатура)
    await message.answer('Выберите действие', reply_markup=start_kb)  # каталог, панель администратора, о нас
    await state.finish()


async def catalog_cmd(message: Message, state: FSMContext):
    await message.answer('Выберите каталог', reply_markup=catalogs_kb)  # wildberries, local
    await state.finish()


async def local_store_cmd(message: Message, state: FSMContext):
    translate_filters = {'gender': 'Пол',
                         'type_of_clothing': 'Тип одежды',
                         'size': 'Размер',
                         'style': 'Стиль',
                         'seasonality': 'Сезонность',
                         'brand': 'Бренд'}
    async with state.proxy() as data:
        filters: dict = data.get('filters', 'not_found')
        if filters == 'not_found':
            data['filters'] = {}
            data['goods_shown'] = []
            text = 'Добавьте фильтры'
        else:
            text = ''
            if filters.get('search', ''):
                text += f'Запрос: {filters["search"]}\n'
            for key, values in filters.items():
                if len(values) != 0:
                    if key not in ('search', 'price_min', 'price_max'):
                        text += f'\n{translate_filters[key]}:'
                        for value in values:
                            text += f'\t🔘{value}\n'
                        text = text[:-1]
            if filters.get('price_min', '') or filters.get('price_max', ''):
                min_price = filters.get('price_min', '')
                max_price = filters.get('price_max', '')
                text += (f"\nЦена "
                         f"{f'от {min_price}р. ' if min_price else ''}"
                         f"{f'до {max_price}р.' if min_price else ''}")
            text += '\n\n⬆⬆⬆выбранные фильтры⬆⬆⬆'

    await message.answer(text, reply_markup=local_store_inline_kb)
    await state.set_state(SearcherFSM.wait_for_local_filter_adjustment.state)


async def filter_adjustment(call: CallbackQuery, state: FSMContext):
    data = call.data.split(':')
    callback_data = {'callback': data[0],
                     'action': data[1],
                     'filter_on_adjustment': data[2]}
    try:
        callback_data['item'] = data[3]  # есть не у всех колбеков, поэтому создается отдельно
    except IndexError:
        pass
    if callback_data['action'] == 'start':
        async with state.proxy() as data:
            filters = data['filters']
        await call.message.edit_text('Выберите нужное',
                                     reply_markup=generate_filters_choose_inline_kb(
                                         # filter_on_adjustment - как название столбца в таблице
                                         filter_on_adjustment=callback_data['filter_on_adjustment'],
                                         exists_filters=filters))
    elif callback_data['action'] == 'add':
        async with state.proxy() as data:
            if callback_data['filter_on_adjustment'] not in data:
                data['filters'][callback_data['filter_on_adjustment']] = [callback_data['item']]  # gender = [male]
            else:
                if callback_data['item'] in data['filters'][callback_data['filter_on_adjustment']]:
                    raise f"{callback_data['item']} already in {data['filters'][callback_data['filter_on_adjustment']]}"
                data['filters'][callback_data['filter_on_adjustment']].append(callback_data['item'])
        async with state.proxy() as data:
            filters = data['filters']
        await call.message.edit_text('Выберите нужное',
                                     reply_markup=generate_filters_choose_inline_kb(
                                         # filter_on_adjustment - как название столбца в таблице
                                         filter_on_adjustment=callback_data['filter_on_adjustment'],
                                         exists_filters=filters))

    elif callback_data['action'] == 'remove':
        async with state.proxy() as data:
            if callback_data['filter_on_adjustment'] not in data:
                raise f'{callback_data["filter_on_adjustment"]} not exists'
            else:
                if callback_data['item'] not in data['filters'][callback_data['filter_on_adjustment']]:
                    raise f"{callback_data['item']} not in {data['filters'][callback_data['filter_on_adjustment']]}"
                data['filters'][callback_data['filter_on_adjustment']].pop(callback_data['item'])
        async with state.proxy() as data:
            filters = data['filters']
        await call.message.edit_text('Выберите нужное',
                                     reply_markup=generate_filters_choose_inline_kb(
                                         # filter_on_adjustment - как название столбца в таблице
                                         filter_on_adjustment=callback_data['filter_on_adjustment'],
                                         exists_filters=filters))  # inline_kb (new regenerated)

    elif callback_data['action'] == 'accept':
        await call.message.edit_text('Ваши фильтры: ', reply_markup=local_store_inline_kb)
    # Далее фильтры перечисляются (только активированные)

    await call.answer()


async def price_adjustment(call: CallbackQuery, state: FSMContext):
    # await call.message.answer('Введите минимальную цену', reply_markup=delete_msg_inline_kb)
    await call.message.answer('Введите минимальную цену')
    await call.message.delete()
    await state.set_state(SearcherFSM.wait_for_local_min_price_adjustment.state)

    await call.answer()


async def min_price_adjustment(message: Message, state: FSMContext):
    text = message.text
    nums = ''
    is_first_num = False
    for symbol in list(text):
        if symbol.isdigit():
            nums += symbol
            is_first_num = True
        elif is_first_num:
            break
    price_min = nums
    if nums != '':
        # await message.answer('Теперь введите максимальную цену', reply_markup=delete_msg_inline_kb)
        await message.answer('Теперь введите максимальную цену')
        async with state.proxy() as data:
            data['filters']['price_min'] = price_min
        # await message.delete()
        await state.set_state(SearcherFSM.wait_for_local_max_price_adjustment.state)
    else:
        # await message.answer('Введите минимальную цену', reply_markup=delete_msg_inline_kb)
        await message.answer('Введите минимальную цену')


async def max_price_adjustment(message: Message, state: FSMContext):
    text = message.text
    nums = ''
    is_first_num = False
    for symbol in list(text):
        if symbol.isdigit():
            nums += symbol
            is_first_num = True
        elif is_first_num:
            break
    price_max = nums
    if nums != '':
        # await message.answer('Записано! Вы можете вернуться к выбору фильтров', reply_markup=delete_msg_inline_kb)
        await message.answer('Записано! Вы можете вернуться к выбору фильтров')
        async with state.proxy() as data:
            data['filters']['price_max'] = price_max
        # await message.delete()
        await local_store_cmd(message, state)
    else:
        # await message.answer('Введите максимальную цену', reply_markup=delete_msg_inline_kb)
        await message.answer('Введите максимальную цену')


# not used yet
async def delete_msg(call: CallbackQuery):
    await call.message.delete()


async def add_search_request(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите поисковый запрос')
    await call.message.delete()

    await state.set_state(SearcherFSM.wait_for_search_request.state)


async def search_request_adjustment(message: Message, state: FSMContext):
    await message.answer('Записано! Можете возвращаться к выбору')
    async with state.proxy() as data:
        data['filters']['search'] = message.text
    await local_store_cmd(message, state)


async def cancel_callback(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено')
    await call.answer()
    await state.finish()
    await start_cmd(message=call.message, state=state)


async def local_find_products(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Идет поиск...')
    # Вывод карточек товаров
    async with state.proxy() as data:
        exists_filters = data['filters']

    request_filter = ''
    for key, values in exists_filters.items():
        request_filter += f'('
        if type(values) == list:
            for value in values:
                request_filter += f'{key}={value} OR '
            try:
                request_filter = request_filter[:-4]
            except:
                request_filter = ''
        elif type(values) == str:
            # request_filter += f'{values} IN description'
            request_filter += f"instr(description, '{values}') != 0"
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
        request_filter += ') AND'
        # try:
        #     request_filter = request_filter[:-4] + ') AND'
        # except:
        #     request_filter = ''
    try:
        request_filter = request_filter[:-4]
    except:
        request_filter = ''

    async with state.proxy() as data:
        goods_shown = data.get('goods_shown', 'not_found')
    if goods_shown:
        request_filter += f' AND (id NOT IN {goods_shown})'

    products = db_worker.products_read(request_filter=request_filter)
    if len(products) == 0:
        await call.message.answer('Кажется такого у нас нет... \n'
                                  'Попробуйте поменять или убрать некоторые параметры в вашем запросе')
    else:
        photo_not_found_v1 = ("https://img.freepik.com/free-vector/flat-design-"
                              "no-photo-sign_23-2149259323.jpg?w=740&t=st"
                              "=1693080680~exp=1693081280~hmac=d75c50532482d7fd7b9"
                              "3cf893a133f7a6c883d1b4f48811ecd8bcb5641fc5b8a")
        photo_not_found_v2 = ("https://static.vecteezy.com/system/resources/previews/"
                              "005/337/799/original/icon-image-not-found-free-vector.jpg")
        for i in range(15):
            if len(products)-i-1 <= 0:
                continue
            (product_id,
             product_name,
             product_photo,
             product_gender,
             product_type_of_clothing,
             product_size,
             product_description,
             product_seasonality,
             product_brand,
             product_price,
             product_url) = products[i]

            card_text = (f"Номер товара: {product_id}.\n"
                         f"{product_description}.\n"
                         f"Пол: {product_gender}\n"
                         f"Тип: {product_type_of_clothing}\n"
                         f"Размер: {product_size}\n"
                         f"Сезон: {product_seasonality}\n"
                         f"Бренд: {product_brand}\n"
                         f"Цена: {product_price}\n"
                         f"Ссылка на товар: {product_url} ")
            try:
                await call.message.answer_photo(photo=product_photo,
                                                caption=card_text,
                                                reply_markup=generate_card_product_kb(need_more_btn=False,
                                                                                      product_id=product_id))
            except WrongFileIdentifier:
                await call.message.answer_photo(photo=photo_not_found_v2, caption=card_text)

            async with state.proxy() as data:
                if data.get('goods_shown') == 'not_found':
                    data['goods_shown'] = list()
                data['goods_shown'].append(product_id)
    await call.message.answer('Если вы хотите вернуться к выбору фильтров - исользуйте /local_shop или /наш_магазин')
    await call.answer()
    await call.message.delete()


async def wildberries_store_cmd(message: Message, state: FSMContext):
    """
    Пока мы не определились в надобности парсинга сайта.
    Функция создана, но не регистрируется в хендлерах
    """
    await message.answer('text', reply_markup=test_kb)
    await state.set_state(SearcherFSM.wait_for_wildberries_filter_adjustment.state)


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(start_cmd,
                                commands=['start'],
                                state='*')
    dp.register_message_handler(catalog_cmd,
                                commands=['catalog', 'каталог'],
                                state='*')

    # local store
    dp.register_message_handler(local_store_cmd,
                                commands=['local_shop', 'наш_магазин'],
                                state='*')

    # price adjustment
    dp.register_callback_query_handler(price_adjustment,
                                       text_startswith='price_adjustment',
                                       state=SearcherFSM.wait_for_local_filter_adjustment)
    dp.register_message_handler(min_price_adjustment,
                                state=SearcherFSM.wait_for_local_min_price_adjustment)
    dp.register_message_handler(max_price_adjustment,
                                state=SearcherFSM.wait_for_local_max_price_adjustment)

    # search request adjustment
    dp.register_callback_query_handler(add_search_request,
                                       text_startswith='search_request_adjustment',
                                       state=SearcherFSM.wait_for_local_filter_adjustment)
    dp.register_message_handler(search_request_adjustment,
                                state=SearcherFSM.wait_for_search_request)

    # other filters adjustment
    dp.register_callback_query_handler(filter_adjustment,
                                       text_startswith='filter_adjustment',
                                       state=SearcherFSM.wait_for_local_filter_adjustment)

    # cancel function
    dp.register_callback_query_handler(cancel_callback,
                                       text_startswith='cancel',
                                       state=SearcherFSM.wait_for_local_filter_adjustment)

    # search cards
    dp.register_callback_query_handler(local_find_products,
                                       text_startswith='search_cards',
                                       state=SearcherFSM.wait_for_local_filter_adjustment)

