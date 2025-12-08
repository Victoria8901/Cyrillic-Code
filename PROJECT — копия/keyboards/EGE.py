from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_EGE_menu_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(4, 22):
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=str(i), 
                    callback_data=f'EGE_task:{i}'
                )
            ]
        )

    return keyboard