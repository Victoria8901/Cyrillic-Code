"""Сервис для работы с объектным хранилищем"""
import os
import logging
from typing import Optional, BinaryIO
from io import BytesIO

try:
    from minio import Minio
    from minio.error import S3Error
    MINIO_AVAILABLE = True
except ImportError:
    MINIO_AVAILABLE = False
    logging.warning("MinIO library not installed. File storage will use local filesystem.")

from config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Сервис для работы с файлами (MinIO или локальная файловая система)"""
    
    def __init__(self):
        self.config = settings.minio
        # По умолчанию используем MinIO, если доступен
        self.use_minio = MINIO_AVAILABLE and os.getenv("USE_MINIO", "true").lower() == "true"
        
        if self.use_minio:
            try:
                self.client = Minio(
                    self.config.endpoint,
                    access_key=self.config.access_key,
                    secret_key=self.config.secret_key,
                    secure=self.config.use_ssl
                )
                # Проверяем существование bucket, создаем если нет
                if not self.client.bucket_exists(self.config.bucket_name):
                    self.client.make_bucket(self.config.bucket_name)
                logger.info(f"MinIO storage initialized: {self.config.endpoint}")
            except Exception as e:
                logger.error(f"Failed to initialize MinIO: {e}")
                self.use_minio = False
        else:
            logger.info("Using local filesystem storage")
    
    def get_file(self, file_path: str) -> Optional[BytesIO]:
        """Получить файл из хранилища"""
        if self.use_minio:
            try:
                data = self.client.get_object(self.config.bucket_name, file_path)
                return BytesIO(data.read())
            except S3Error as e:
                logger.error(f"Error getting file from MinIO: {e}")
                return None
        else:
            # Локальная файловая система
            full_path = os.path.join("bot/data", file_path)
            if os.path.exists(full_path):
                with open(full_path, "rb") as f:
                    return BytesIO(f.read())
            return None
    
    def save_file(self, file_path: str, file_data: BinaryIO) -> bool:
        """Сохранить файл в хранилище"""
        if self.use_minio:
            try:
                file_data.seek(0, 2)  # Перемещаемся в конец файла
                file_size = file_data.tell()  # Получаем размер
                file_data.seek(0)  # Возвращаемся в начало
                
                self.client.put_object(
                    self.config.bucket_name,
                    file_path,
                    file_data,
                    length=file_size
                )
                file_data.seek(0)
                return True
            except S3Error as e:
                logger.error(f"Error saving file to MinIO: {e}")
                return False
        else:
            # Локальная файловая система
            full_path = os.path.join("bot/data", file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "wb") as f:
                file_data.seek(0)
                f.write(file_data.read())
            return True
    
    def file_exists(self, file_path: str) -> bool:
        """Проверить существование файла"""
        if self.use_minio:
            try:
                self.client.stat_object(self.config.bucket_name, file_path)
                return True
            except S3Error:
                return False
        else:
            full_path = os.path.join("bot/data", file_path)
            return os.path.exists(full_path)


# Глобальный экземпляр сервиса
storage_service = StorageService()

