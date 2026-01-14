"""Главный файл запуска бота"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from bot.handlers import register_routes

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    if not settings.bot.token:
        logger.error("BOT_TOKEN не установлен! Проверьте файл .env")
        return
    
    # Применение миграций БД (если нужно)
    try:
        from bot.utils.apply_migrations import apply_migrations
        logger.info("Проверка миграций БД...")
        apply_migrations()
    except Exception as e:
        logger.error(f"Ошибка при применении миграций: {e}")
        logger.warning("Бот продолжит работу, но могут быть проблемы с БД")
    
    # Инициализация хранилища (загрузка файлов в MinIO при первом запуске)
    try:
        from bot.utils.init_storage import init_storage
        init_storage()
    except Exception as e:
        logger.warning(f"Ошибка при инициализации хранилища: {e}")
    
    # Инициализация бота и диспетчера
    bot = Bot(token=settings.bot.token)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация роутеров
    register_routes(dp)
    
    logger.info("Бот запущен")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Бот остановлен!')

