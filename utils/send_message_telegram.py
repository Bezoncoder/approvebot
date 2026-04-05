from typing import List
from aiogram import Bot
from aiogram.types import FSInputFile
from get_data_settings.get_config import TextButton, InlineButton
from important.reliability import send_video, send_photo, send_message
from keyboards.inline import get_inline_keyboards
from keyboards.reply import get_text_keyboards
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

media_data = {}


async def send_message_telegram(bot: Bot, chat_id: int, path_file: str, post_text: str,
                                inline_buttons: List[InlineButton], text_buttons: List[TextButton]):
    logger.info("Sending message...")
    keyboard = None
    if len(inline_buttons) > 0:
        keyboard = get_inline_keyboards(buttons=inline_buttons)
    if len(text_buttons) > 0:
        keyboard = get_text_keyboards(buttons=text_buttons)
    if path_file != '':
        if path_file in media_data:
            upload_file = media_data[path_file]
            logger.info(f"Found cached media file for {path_file}: {upload_file}")
        else:
            upload_file = FSInputFile(path=path_file)
            logger.info(f"Uploading media file: {path_file}")
        if path_file.lower().endswith(('png', 'jpg', 'jpeg')):
            logger.info("Sending photo...")
            message = await send_photo(bot=bot, chat_id=chat_id, photo=upload_file, caption=post_text, reply_markup=keyboard)
            media_data[path_file] = message.photo[-1].file_id
        elif path_file.lower().endswith(('mp4', 'avi', 'mkv', 'mpg', 'mpeg')):
            logger.info("Sending video...")
            message = await send_video(bot=bot, chat_id=chat_id, video=upload_file, caption=post_text, reply_markup=keyboard)
            media_data[path_file] = message.video.file_id
        logger.info("Message sent successfully.")
    else:
        await send_message(bot=bot, chat_id=chat_id, text=post_text, reply_markup=keyboard)