"""Сервис для работы с локальным хранилищем файлов."""
import os
from typing import Optional, BinaryIO
from io import BytesIO
from pathlib import Path


class StorageService:
    """Сервис для работы с файлами (локальная файловая система)."""

    def __init__(self):
        self.base_path = Path("bot/data")

    def get_file(self, file_path: str) -> Optional[BytesIO]:
        """Получить файл из хранилища."""
        full_path = self.base_path / file_path
        if full_path.exists():
            with open(full_path, "rb") as f:
                return BytesIO(f.read())
        return None

    def save_file(self, file_path: str, file_data: BinaryIO) -> bool:
        """Сохранить файл в хранилище."""
        full_path = self.base_path / file_path
        os.makedirs(full_path.parent, exist_ok=True)
        with open(full_path, "wb") as f:
            file_data.seek(0)
            f.write(file_data.read())
        return True

    def file_exists(self, file_path: str) -> bool:
        """Проверить существование файла."""
        return (self.base_path / file_path).exists()


# Глобальный экземпляр сервиса
storage_service = StorageService()
