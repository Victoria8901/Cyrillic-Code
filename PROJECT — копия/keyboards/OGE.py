from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_OGE_menu_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(2, 10):
        keyboard.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=str(i), 
                    callback_data=f'OGE_task:{i}'
                )
            ]
        )

    return keyboard