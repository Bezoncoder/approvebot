from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.dbconnect import Request
from utils.send_message_telegram import send_message_telegram


async def answer_dice(message: Message, bot: Bot, request: Request, apscheduler: AsyncIOScheduler):
    result = await message.answer_dice(emoji=message.dice.emoji)
    if result.dice.value < message.dice.value:
        text_result = f'Мой респект, ты выйграл! Возвращайся снова.'
    elif result.dice.value > message.dice.value:
        text_result = f'Победа за мной! Возвращайся снова.'
    else:
        text_result = f'Ничья. Еще разок?'
    time_run = datetime.now() + timedelta(seconds=5)
    apscheduler.add_job(
        func=send_message_telegram,
        trigger='date',
        run_date=time_run,
        kwargs={'chat_id': message.from_user.id,
                'post_text': text_result,
                'path_file': '',
                'inline_buttons': [],
                'text_buttons': []}
    )
    await request.add_user(user_id=message.chat.id)