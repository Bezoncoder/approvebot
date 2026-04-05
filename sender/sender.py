import contextlib
import logging
from datetime import datetime, timedelta
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from important.reliability import send_message, edit_message, copy_message
from sender.check_latin import is_latin_only
from sender.check_link import check_link
from sender.inline import get_confirm_button_keyboard
from sender.sender_state import Steps
from utils.dbconnect import Request


async def get_sender(message: Message, bot: Bot, command: CommandObject, state: FSMContext):
    if not command.args:
        await send_message(bot=bot, chat_id=message.from_user.id,
                           text=f'Для создания кампании введи команду /sender и имя кампании.'
                                f'Например, /sender earlybirds')
        return
    if not await is_latin_only(text=command.args):
        await send_message(bot=bot, chat_id=message.from_user.id,
                           text=f'Допускаются, только латинские символы нижнего регистра в имени кампании.')
        return
    await send_message(bot=bot, chat_id=message.from_user.id,
                       text=f'Приступаем создавать компанию для рассылки. Имя кампании - {command.args}\r\n\r\n'
                            f'Отправь мне сообшение, которое будет использовано, как рекламное.')
    await state.update_data(name_company=command.args)
    await state.set_state(Steps.get_message)


async def get_message(message: Message, bot: Bot, state: FSMContext):
    await send_message(bot=bot, chat_id=message.from_user.id,
                       text=f'Ок, я запомнил сообщение, которое ты хочешь разослать.\r\nКнопку будем добовлять?',
                       reply_markup=get_confirm_button_keyboard())
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    await state.set_state(Steps.q_button)


async def q_button(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data == 'add_button':
        await edit_message(bot=bot,
                           text='Отправь текст для кнопки',
                           chat_id=call.message.chat.id,
                           message_id=call.message.message_id,
                           reply_markup=None)
        await state.set_state(Steps.get_text_button)
    elif call.data == 'no_button':
        await call.message.edit_reply_markup(reply_markup=None)
        await time_confirm(call.message, bot, int((await state.get_data()).get('message_id')),
                           int((await state.get_data()).get('chat_id')))

    await call.answer()


async def get_text_button(message: Message, state: FSMContext):
    await state.update_data(text_button=message.text)
    await message.answer(f'Теперь отправь ссылку.')
    await state.set_state(Steps.get_url_button)


async def get_url_button(message: Message, bot: Bot, state: FSMContext):
    if not check_link(url=message.text):
        await message.answer(f'Ссылка {message.text} не корректна. Введи ссылку еще раз.')

    await state.update_data(url_button=message.text)
    added_keyboards = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=(await state.get_data()).get('text_button'),
        url=f'{message.text}')]])
    await time_confirm(message, bot, int((await state.get_data()).get('message_id')),
                       int((await state.get_data()).get('chat_id')), added_keyboards)


async def time_confirm(message: Message, bot: Bot, message_id: int, chat_id: int,
                       reply_markup: InlineKeyboardMarkup = None):
    copy_message = await bot.copy_message(chat_id, chat_id, message_id, reply_markup=reply_markup)
    with contextlib.suppress(TelegramBadRequest):
        await send_message(bot=bot, chat_id=message.chat.id,
                           text=f'Вот сообщение, которое будем рассылать. Подтверди.',
                           reply_to_message_id=copy_message.message_id,
                           reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                               [InlineKeyboardButton(
                                   text='Подтвердить',
                                   callback_data=f'confirm_message')],
                               [InlineKeyboardButton(
                                   text='Отменить',
                                   callback_data=f'cancel_message')]]))


async def confirm_message(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    data = await state.get_data()
    name_company = data.get('name_company')
    await request.create_table_sender(name_table=name_company)
    count_users_sender = await request.get_count_sender(name_company=name_company)
    await edit_message(bot=bot, text=f'Рекламное сообщение будет расослано {count_users_sender} пользователям.'
                                     f'Начинаем рассылку?',
                       chat_id=call.message.chat.id,
                       message_id=call.message.message_id,
                       reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                           InlineKeyboardButton(
                               text='Подтвердить',
                               callback_data=f'start_sender')],
                            [InlineKeyboardButton(
                                text='Отменить',
                                callback_data=f'cancel_sender')]]))


async def cancel_message(call: CallbackQuery, bot: Bot, state: FSMContext):
    await edit_message(bot=bot,
                       text=f'Отменил рассылку',
                       chat_id=call.message.message_id,
                       reply_markup=None)
    await state.clear()


async def start_sender(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request,
                       apscheduler: AsyncIOScheduler):
    await call.answer()
    data = await state.get_data()
    message_id = data.get('message_id')
    chat_id = data.get('chat_id')
    text_button = data.get('text_button') if data.get('text_button') else ''
    url_button = data.get('url_button') if data.get('url_button') else ''
    name_company = data.get('name_company')
    await edit_message(bot=bot,
                       text=f'Создаю задания для рассылки.',
                       chat_id=call.message.chat.id,
                       message_id=call.message.message_id,
                       reply_markup=None)
    time_run = datetime.now() + timedelta(seconds=10)
    users_ids = await request.get_users(name_company=name_company)
    count = 0
    for user_id in users_ids:
        apscheduler.add_job(func=send_message_to_user,
                            trigger='date',
                            run_date=time_run,
                            misfire_grace_time=3600,
                            kwargs={'user_id': user_id,
                                    'from_chat_id': chat_id,
                                    'message_id': message_id,
                                    'text_button': text_button,
                                    'url_button': url_button})
        time_run += timedelta(seconds=.1)
        count += 1
    await send_message(bot=bot,
                       chat_id=call.message.chat.id,
                       text=f'Задание успешно создано для {count} пользователей',
                       reply_markup=None)
    await state.clear()
    await request.delete_table(name_table=name_company)


async def send_message_to_user(bot: Bot, user_id: int, from_chat_id: int, message_id: int, text_button: str,
                               url_button: str):
    try:
        keyboard = None
        if text_button != '' and url_button != '':
            keyboard_builder = InlineKeyboardBuilder()
            keyboard_builder.button(text=text_button, url=url_button)
            keyboard_builder.adjust(1)
            keyboard = keyboard_builder.as_markup()
        await copy_message(bot=bot, chat_id=user_id, from_chat_id=from_chat_id, message_id=message_id,
                           reply_markup=keyboard, max_retries=3)
        logging.info(f'Успешно отправили сообщение пользователю [{user_id}]')
    except Exception as exc:
        logging.error(f'Не удалось отправить сообщение пользователю [{user_id}] - {exc}')


async def cancel_sender(call: CallbackQuery, bot: Bot, state: FSMContext, request: Request):
    data = await state.get_data()
    name_company = data.get('name_company')
    await edit_message(bot=bot,
                       text=f'Отменил рассылку',
                       chat_id=call.message.message_id,
                       reply_markup=None)
    await request.delete_table(name_table=name_company)
    await state.clear()
