"""Регистрация всех роутеров"""
from aiogram import Dispatcher

from bot.handlers.start import router as start_router
from bot.handlers.info import router as info_router
from bot.handlers.help import router as help_router
from bot.handlers.oge import router as oge_router
from bot.handlers.ege import router as ege_router


def register_routes(dp: Dispatcher):
    """Регистрация всех роутеров"""
    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(help_router)
    dp.include_router(oge_router)
    dp.include_router(ege_router)

