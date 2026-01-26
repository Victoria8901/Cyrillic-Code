"""Конфигурация приложения"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class DatabaseConfig:
    """Конфигурация базы данных"""
    host: str = os.getenv("DB_HOST", "localhost")
    port: int = int(os.getenv("DB_PORT", "5432"))
    database: str = os.getenv("DB_NAME", "oge_ege_bot")
    user: str = os.getenv("DB_USER", "bot_user")
    password: str = os.getenv("DB_PASSWORD", "bot_password")


@dataclass
class BotConfig:
    """Конфигурация бота"""
    token: str = os.getenv("BOT_TOKEN", "")
    admin_ids: list[int] = None

    def __post_init__(self):
        if self.admin_ids is None:
            admin_str = os.getenv("ADMIN_IDS", "")
            self.admin_ids = [int(id_) for id_ in admin_str.split(",") if id_] if admin_str else []


@dataclass
class Settings:
    """Общие настройки приложения"""
    db: DatabaseConfig = None
    bot: BotConfig = None

    def __post_init__(self):
        if self.db is None:
            self.db = DatabaseConfig()
        if self.bot is None:
            self.bot = BotConfig()


# Глобальный экземпляр настроек
settings = Settings()

