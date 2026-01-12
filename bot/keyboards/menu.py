"""Клавиатуры главного меню"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_kb():
    """Главное меню бота"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Подготовка к ОГЭ')],
            [KeyboardButton(text='Подготовка к ЕГЭ')],
            [KeyboardButton(text='Мой профиль'), KeyboardButton(text='Помощь')],
        ],
        resize_keyboard=True
    )

