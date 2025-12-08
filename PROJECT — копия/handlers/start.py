from aiogram import Router, types
from aiogram.filters import Command

from keyboards.menu import main_menu_kb
from handlers.db_handler import load_db

import json
import os

router = Router()

conn_db = load_db()
cursor = conn_db.cursor()

@router.message(Command('start'))
async def start(message: types.Message):

    chat_id = message.from_user.id
    name = message.from_user.full_name
    countOGE = 0
    countEGE = 0
    cursor.execute( f"SELECT 1 FROM users WHERE chat_id = '{chat_id}'")
    res = cursor.fetchall()
    if len(res) == 0:
        cursor.execute('INSERT INTO users (name, chat_id, count_oge, count_ege) VALUES (%s, %s, %s, %s);', (name, chat_id, countOGE, countEGE))
    conn_db.commit()
    await message.answer(f'Привет, {message.from_user.full_name}\nЯ бот, который поможет подготовиться к русскому языку!',
                         reply_markup=main_menu_kb()
    )

