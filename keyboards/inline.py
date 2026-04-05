from typing import List
from aiogram.utils.keyboard import InlineKeyboardBuilder
from get_data_settings.get_config import InlineButton
import logging

logger = logging.getLogger(__name__)


def get_inline_keyboards(buttons: List[InlineButton]):
    if len(buttons) > 0:
        keyboards_builder = InlineKeyboardBuilder()
        for button in buttons:
            keyboards_builder.button(text=button.text_button, url=button.url_button)
        keyboards_builder.adjust(1)
        logger.info('Keyboards created.')
        return keyboards_builder.as_markup()
    else:
        return None
