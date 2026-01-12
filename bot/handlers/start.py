"""Обработчик команды /start"""
from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards.menu import main_menu_kb
from bot.services.database import db_service

router = Router()


@router.message(Command('start'))
async def start_handler(message: types.Message):
    """Обработчик команды /start"""
    chat_id = message.from_user.id
    name = message.from_user.full_name or "Пользователь"
    
    # Получаем или создаем пользователя
    user = db_service.get_or_create_user(chat_id, name)
    
    await message.answer(
        f'Привет, {name}!\n'
        'Я бот, который поможет подготовиться к русскому языку!',
        reply_markup=main_menu_kb()
    )

