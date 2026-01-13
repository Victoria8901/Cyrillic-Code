"""Клавиатуры для ЕГЭ"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_ege_menu_kb():
    """Генерация клавиатуры с заданиями ЕГЭ"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(4, 22):
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Задание {i}",
                    callback_data=f"ege_task:{i}"
                )
            ]
        )

    return keyboard


