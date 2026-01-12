"""Обработчик профиля пользователя"""
from aiogram import Router, types
from aiogram.filters import Command

from bot.services.database import db_service

router = Router()


@router.message(lambda message: message.text == 'Мой профиль')
async def profile_handler(message: types.Message):
    """Обработчик просмотра профиля"""
    chat_id = message.from_user.id
    user = db_service.get_user_by_chat_id(chat_id)
    
    if not user:
        await message.answer("Вы не зарегистрированы. Используйте /start")
        return
    
    # Получаем статистику
    oge_progress = db_service.get_user_progress(user["user_id"], "OGE")
    ege_progress = db_service.get_user_progress(user["user_id"], "EGE")
    
    text = (
        f"📊 Ваш профиль\n\n"
        f"👤 Имя: {user['name']}\n"
        f"📚 ОГЭ: пройдено {oge_progress['completed_count']} из {oge_progress['total_count']} тем\n"
        f"📖 ЕГЭ: пройдено {ege_progress['completed_count']} из {ege_progress['total_count']} тем"
    )
    
    await message.answer(text)

