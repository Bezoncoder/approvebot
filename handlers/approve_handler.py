from datetime import timedelta, datetime
from aiogram import Bot
from aiogram.types import ChatJoinRequest, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from get_data_settings.get_ads_posts import get_posts_by_chat_id
from important.reliability import send_message
from utils.dbconnect import Request
from utils.send_message_telegram import send_message_telegram
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

media_data = {}


async def approve_request(chat_join: ChatJoinRequest, bot: Bot, apscheduler: AsyncIOScheduler):
    logger.info("Approving request...")
    try:
        await chat_join.approve()
    except:
        pass
    posts = get_posts_by_chat_id(target_chat_id=chat_join.chat.id)
    time_run = datetime.now()
    logger.info(f"Found {len(posts)} posts for chat ID {chat_join.chat.id}")
    for post in posts:
        time_run += timedelta(seconds=post.delay)
        logger.info(f"Scheduling message for post: {post.path_media}")
        apscheduler.add_job(func=send_message_telegram, trigger='date', run_date=time_run, kwargs={
            'chat_id': chat_join.from_user.id,
            'post_text': post.post_text,
            'path_file': post.path_media if post.path_media else '',
            'inline_buttons': post.inline_buttons if post.inline_buttons else [],
            'text_buttons': post.text_buttons if post.text_buttons else []})


async def confirm_human(message: Message, bot: Bot, request: Request):
    await send_message(bot=bot, chat_id=message.chat.id, text='Окб спасибо за подтверждение.')
    await request.add_user(user_id=message.chat.id)

