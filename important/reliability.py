import asyncio
import logging
from typing import Union, Any
from aiogram import Bot
from aiogram.client.default import Default
from aiogram.exceptions import TelegramRetryAfter, TelegramNetworkError, TelegramBadRequest
from aiogram.types import MessageEntity, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, \
    ForceReply, Message, InputFile, ReplyParameters, LinkPreviewOptions
from aiogram.types.base import UNSET, UNSET_PROTECT_CONTENT, UNSET_PARSE_MODE

logger = logging.getLogger(__name__)


async def send_message(
        bot: Bot,
        chat_id: int,
        text: str,
        parse_mode: str = 'HTML',
        entities: list[MessageEntity] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        protect_content: bool = None,
        reply_to_message_id: int = None,
        allow_sending_without_reply: bool = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        request_timeout: int | None = None) -> Union[Message, Any]:
    for i in range(10):
        try:
            message = await bot.send_message(chat_id=chat_id,
                                             text=text,
                                             parse_mode=parse_mode,
                                             entities=entities,
                                             disable_web_page_preview=disable_web_page_preview,
                                             disable_notification=disable_notification,
                                             protect_content=protect_content,
                                             reply_to_message_id=reply_to_message_id,
                                             allow_sending_without_reply=allow_sending_without_reply,
                                             reply_markup=reply_markup,
                                             request_timeout=request_timeout)
            logger.info('Photo sent successfully.')
            return message
        except TelegramRetryAfter as e:
            logging.error(f"TelegramRetryAfter: {e}")
            await asyncio.sleep(e.retry_after)
        except TelegramNetworkError as e:
            logging.error(f"TelegramNetworkError: {e}")
            await asyncio.sleep(5)
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest: {e}")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Exception: {e}")
            await asyncio.sleep(5)
    raise Exception("Не удалось отправить фото. Читай лог!")


async def send_photo(
        bot: Bot,
        chat_id: int | str,
        photo: InputFile | str,
        message_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = UNSET_PARSE_MODE,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = UNSET_PROTECT_CONTENT,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        allow_sending_without_reply: bool | None = None,
        reply_to_message_id: int | None = None,
        request_timeout: int | None = None) -> Union[Message, Any]:
    for i in range(10):
        try:
            message = await bot.send_photo(chat_id=chat_id, photo=photo, message_thread_id=message_thread_id,
                                           caption=caption, parse_mode=parse_mode, caption_entities=caption_entities,
                                           has_spoiler=has_spoiler, disable_notification=disable_notification,
                                           protect_content=protect_content, reply_parameters=reply_parameters,
                                           reply_to_message_id=reply_to_message_id,
                                           allow_sending_without_reply=allow_sending_without_reply,
                                           reply_markup=reply_markup, request_timeout=request_timeout)
            logger.info('Photo sent successfully.')
            return message
        except TelegramRetryAfter as e:
            logging.error(f"TelegramRetryAfter: {e}")
            await asyncio.sleep(e.retry_after)
        except TelegramNetworkError as e:
            logging.error(f"TelegramNetworkError: {e}")
            await asyncio.sleep(5)
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest: {e}")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Exception: {e}")
            await asyncio.sleep(5)
    raise Exception("Не удалось отправить фото. Читай лог!")


async def send_video(
        bot: Bot,
        chat_id: int | str,
        video: InputFile | str,
        message_thread_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: InputFile | None = None,
        caption: str | None = None,
        parse_mode: str | None = UNSET,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: bool | None = None,
        supports_streaming: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = UNSET_PROTECT_CONTENT,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        allow_sending_without_reply: bool | None = None,
        reply_to_message_id: int | None = None,
        request_timeout: int | None = None) -> Union[Message, Any]:
    for i in range(10):
        try:
            message = await bot.send_video(chat_id=chat_id, video=video, message_thread_id=message_thread_id,
                                           duration=duration, width=width, height=height, thumbnail=thumbnail,
                                           caption=caption, parse_mode=parse_mode, caption_entities=caption_entities,
                                           has_spoiler=has_spoiler, supports_streaming=supports_streaming,
                                           disable_notification=disable_notification, protect_content=protect_content,
                                           reply_parameters=reply_parameters, reply_to_message_id=reply_to_message_id,
                                           allow_sending_without_reply=allow_sending_without_reply,
                                           reply_markup=reply_markup, request_timeout=request_timeout)
            logger.info('Video sent successfully.')
            return message
        except TelegramRetryAfter as e:
            logging.error(f"TelegramRetryAfter: {e}")
            await asyncio.sleep(e.retry_after)
        except TelegramNetworkError as e:
            logging.error(f"TelegramNetworkError: {e}")
            await asyncio.sleep(5)
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest: {e}")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Exception: {e}")
            await asyncio.sleep(5)
    raise Exception("Не удалось отправить видео. Читай лог!")


async def edit_message(
        bot: Bot,
        text: str,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        parse_mode: str | Default | None = Default("parse_mode"),
        entities: list[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        disable_web_page_preview: bool | Default | None = Default("link_preview_is_disabled"),
        request_timeout: int | None = None
) -> Union[Message, bool]:
    for i in range(10):
        try:
            message = await bot.edit_message_text(chat_id=chat_id,
                                                  text=text,
                                                  message_id=message_id,
                                                  inline_message_id=inline_message_id,
                                                  link_preview_options=link_preview_options,
                                                  parse_mode=parse_mode,
                                                  entities=entities,
                                                  disable_web_page_preview=disable_web_page_preview,
                                                  reply_markup=reply_markup,
                                                  request_timeout=request_timeout)
            logger.info('Photo sent successfully.')
            return message
        except TelegramRetryAfter as e:
            logging.error(f"TelegramRetryAfter: {e}")
            await asyncio.sleep(e.retry_after)
        except TelegramNetworkError as e:
            logging.error(f"TelegramNetworkError: {e}")
            await asyncio.sleep(5)
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest: {e}")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Exception: {e}")
            await asyncio.sleep(5)
    raise Exception("Не удалось отправить фото. Читай лог!")


async def copy_message(
        bot: Bot,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        massage_thread_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = UNSET_PARSE_MODE,
        caption_entities: list[MessageEntity] | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = UNSET_PROTECT_CONTENT,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None,
        allow_sending_without_reply: bool | None = None,
        reply_to_message_id: int | None = None,
        request_timeout: int | None = None,
        max_retries: int = 5):
    for retry in range(max_retries):
        try:
            message = await bot.copy_message(chat_id=chat_id,
                                             from_chat_id=from_chat_id,
                                             message_id=message_id,
                                             message_thread_id=massage_thread_id,
                                             caption=caption,
                                             parse_mode=parse_mode,
                                             caption_entities=caption_entities,
                                             disable_notification=disable_notification,
                                             protect_content=protect_content,
                                             reply_parameters=reply_parameters,
                                             reply_markup=reply_markup,
                                             reply_to_message_id=reply_to_message_id,
                                             allow_sending_without_reply=allow_sending_without_reply,
                                             request_timeout=request_timeout)
            logger.info('Photo sent successfully.')
            return message
        except TelegramRetryAfter as e:
            logging.error(f"TelegramRetryAfter: {e}")
            await asyncio.sleep(e.retry_after)
        except TelegramNetworkError as e:
            logging.error(f"TelegramNetworkError: {e}")
            await asyncio.sleep(5)
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest: {e}")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Exception: {e}")
            await asyncio.sleep(5)
    raise Exception("Не удалось отправить фото. Читай лог!")
