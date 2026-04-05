import sys
from logging.handlers import RotatingFileHandler
import psycopg
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from psycopg_pool import AsyncConnectionPool
from aiogram import Bot, Dispatcher, F
import asyncio
import logging
import contextlib
from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator
from get_data_settings.get_chat_ids import get_all_chat_ids
from get_data_settings.get_config import config
from handlers.approve_handler import approve_request, confirm_human
from handlers.dice import answer_dice
from middlewares.apschedulermiddleware import SchedulerMiddleware
from middlewares.dbmiddleware import DbSession
from middlewares.throttling import ThrottlingMiddleware
from sender import sender
from sender.sender import Steps

file_handler = RotatingFileHandler('bot_logging.log', maxBytes=500000, backupCount=1)
console_handler = logging.StreamHandler()
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler],
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
logger = logging.getLogger(__name__)


async def start_bot(bot: Bot):
    logger.info('Bot started successfully.')
    await bot.send_message(chat_id=config.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    logger.info('Bot stopped.')
    await bot.send_message(chat_id=config.admin_id, text='Бот остановлен!')


async def create_db():
    print(f"Host: {config.db.host}")
    print(f"User: {config.db.user}")
    print(f"Password: {config.db.password}")
    print(f"Database: {config.db.database}")
    conn = psycopg.connect(f'host={config.db.host} port=5432 user={config.db.user}'
                           f'password = {config.db.password} connect_timeout=10')
    conn.autocommit = True
    curs = conn.cursor()
    try:
        curs.execute(f'CREATE DATABASE {config.db.database} WITH OWNER = {config.db.user} ENCODING = \'UTF8\'')
    except Exception as exc:
        logging.error(f"[!!! Exception] - {exc}", exc_info=True)
    finally:
        conn.close()
        curs.close()
    print(f"Host: {config.db.host}")
    print(f"User: {config.db.user}")
    print(f"Password: {config.db.password}")
    print(f"Database: {config.db.database}")
    connect = f"host={config.db.host} port = 5432 dbname={config.db.database} user = {config.db.user}" \
              f"password={config.db.password} connect_timeout=10"
    async with await psycopg.AsyncConnection.connect(conninfo=connect, autocommit=True) as conn:
        async with conn.cursor() as curs:
            await curs.execute(""" CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY);""")


async def start():
    logger.info('Starting bot...')
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    dp = Dispatcher(storage=storage)
    print(f"Host: {config.db.host}")
    print(f"User: {config.db.user}")
    print(f"Password: {config.db.password}")
    print(f"Database: {config.db.database}")
    pooling = AsyncConnectionPool(conninfo=f"host={config.db.host} "
                                           f"port=5432 "
                                           f"dbname={config.db.database} "
                                           f"user={config.db.user} "
                                           f"password={config.db.password} "
                                           f"connect_timeout=10", open=False)
    await pooling.open()
    pooling.connection_class.autocommit = True
    job_stores = {'default': RedisJobStore(jobs_key='dispatched_trips_jobs', run_times_key='dispatched_trips_running',
                                           host='localhost', db=2, port=6379)}
    apscheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Asia/Vladivostok', jobstores=job_stores))
    apscheduler.ctx.add_instance(instance=bot, declared_class=Bot)
    apscheduler.ctx.add_instance(instance=apscheduler, declared_class=AsyncIOScheduler)
    apscheduler.start()
    dp.update.middleware.register(SchedulerMiddleware(apscheduler))
    dp.update.middleware.register(DbSession(pooling))
    dp.message.middleware.register(ThrottlingMiddleware(storage=storage))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    chats_join_request = get_all_chat_ids()
    dp.chat_join_request.register(approve_request, F.chat.id.in_(chats_join_request))
    dp.message.register(confirm_human, F.text == 'Я человек')
    dp.message.register(answer_dice, F.dice)
    dp.message.register(sender.get_sender, Command(commands='sender'), F.chat.id == config.admin_id)
    dp.message.register(sender.get_message, Steps.get_message, F.chat.id == config.admin_id)
    dp.callback_query.register(sender.confirm_message, F.data == 'confirm_message', F.from_user.id == config.admin_id)
    dp.callback_query.register(sender.cancel_message, F.data == 'cancel_message', F.from_user.id == config.admin_id)
    dp.callback_query.register(sender.start_sender, F.data == 'start_sender', F.from_user.id == config.admin_id)
    dp.callback_query.register(sender.cancel_sender, F.data == 'cancel_sender', F.from_user.id == config.admin_id)
    dp.callback_query.register(sender.q_button, Steps.q_button, F.from_user.id == config.admin_id)
    dp.message.register(sender.get_text_button, Steps.get_text_button, F.chat.id == config.admin_id, F.text)
    dp.message.register(sender.get_url_button, Steps.get_url_button, F.chat.id == config.admin_id, F.text)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as exc:
        logger.error(f'[Exception] - {exc}', exc_info=True)
    finally:
        await bot.session.close()
        await pooling.close()


if __name__ == '__main__':
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        console_handler = logging.StreamHandler()
        file_handler = RotatingFileHandler('bot_logging.log', maxBytes=500000, backupCount=1)
        logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler],
                            format="%(asctime)s - [%(levelname)s] - %(name)s - "
                                   "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
