from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Подготовка к ОГЭ')],
        [KeyboardButton(text='Подготовка к ЕГЭ')],
        [KeyboardButton(text='Мой профиль'), KeyboardButton(text='Помощь')],
        ],
        resize_keyboard=True
        )