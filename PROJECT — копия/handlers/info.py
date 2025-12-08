from aiogram import F, Router, types
from aiogram.filters import Command
from handlers.db_handler import load_db

import json

router = Router()
conn_db = load_db()
cursor = conn_db.cursor()

@router.message(F.text == 'Мой профиль')
async def info(message: types.Message):

    chat_id = message.from_user.id
    cursor.execute(f"SELECT * FROM users WHERE chat_id = '{chat_id}'")

    user = cursor.fetchone()

    await message.answer(
        (
            f'имя: {user[1]}\n'
            f'пройдено тем ОГЭ: {user[3]}\n'
            f'пройдено тем ЕГЭ: {user[4]}\n'
        )
    )