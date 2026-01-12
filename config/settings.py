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
class MinIOConfig:
    """Конфигурация MinIO"""
    endpoint: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    bucket_name: str = os.getenv("MINIO_BUCKET", "oge-ege-files")
    use_ssl: bool = os.getenv("MINIO_USE_SSL", "false").lower() == "true"


@dataclass
class RedisConfig:
    """Конфигурация Redis"""
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    db: int = int(os.getenv("REDIS_DB", "0"))
    password: str = os.getenv("REDIS_PASSWORD", "")


@dataclass
class Settings:
    """Общие настройки приложения"""
    db: DatabaseConfig = None
    bot: BotConfig = None
    minio: MinIOConfig = None
    redis: RedisConfig = None

    def __post_init__(self):
        if self.db is None:
            self.db = DatabaseConfig()
        if self.bot is None:
            self.bot = BotConfig()
        if self.minio is None:
            self.minio = MinIOConfig()
        if self.redis is None:
            self.redis = RedisConfig()


# Глобальный экземпляр настроек
settings = Settings()

