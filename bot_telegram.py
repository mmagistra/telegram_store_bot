import logging
from aiogram import executor
from create_bot import dp, db_worker
from handlers.user_handlers import register_user_handlers
from handlers.admin_handlers import register_admin_handlers


logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    print('bot is online')


async def on_shutdown(_):
    db_worker.shutdown()
    print('bot is offline')


register_user_handlers(dp)
register_admin_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
