from typing import List
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from get_data_settings.get_config import TextButton


def get_text_keyboards(buttons: List[TextButton]):
    if len(buttons) > 0:
        keyboard_builder = ReplyKeyboardBuilder()
        for button in buttons:
            dices = {
                'DICE': '🎲',
                'DART': '🎯',
                'BASKETBALL': '🏀',
                'FOOTBALL': '⚽',
                'SLOT_MACHINE': '🎰',
                'BOWLING': '🎳'
            }
            button_text = dices.get(button.text_button, button.text_button)
            keyboard_builder.button(text=button_text)
        keyboard_builder.adjust(1, 6)
        return keyboard_builder.as_markup(resize_keyboard=True,
                                          one_time_keyboards=True,
                                          input_field_placeholder='Подтверди, что ты человек')
    else:
        return None
