"""Клавиатуры для ОГЭ"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_oge_menu_kb():
    """Генерация клавиатуры с заданиями ОГЭ"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(2, 10):
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Задание {i}",
                    callback_data=f"oge_task:{i}"
                )
            ]
        )

    return keyboard


def get_task_actions_kb(task_number: int):
    """Клавиатура действий с заданием"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data=f"solve_task:{task_number}"),
                InlineKeyboardButton(text='Нет', callback_data='oge_menu')
            ]
        ]
    )


def get_continue_solving_kb(task_number: int):
    """Клавиатура для продолжения решения"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да', callback_data=f"solve_task:{task_number}"),
                InlineKeyboardButton(text='Нет', callback_data='oge_menu')
            ]
        ]
    )


def get_test_start_kb(task_number: int):
    """Клавиатура для начала теста"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Начать тест', callback_data=f"oge_test:{task_number}")]
        ]
    )


