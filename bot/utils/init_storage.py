"""Инициализация хранилища - загрузка файлов в MinIO при первом запуске"""
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def init_storage():
    """Инициализировать хранилище - загрузить файлы в MinIO если нужно"""
    from bot.services.storage import storage_service
    
    if not storage_service.use_minio:
        logger.info("MinIO не используется, пропускаем инициализацию")
        return
    
    # Проверяем, есть ли уже файлы в MinIO
    test_path = "OGE/task2/1.txt"
    if storage_service.file_exists(test_path):
        logger.info("Файлы уже загружены в MinIO")
        return
    
    # Проверяем наличие локальных файлов
    data_path = Path("bot/data")
    if not data_path.exists():
        logger.warning(f"Директория {data_path} не найдена, пропускаем загрузку")
        return
    
    logger.info("Начинаем загрузку файлов в MinIO...")
    
    uploaded = 0
    errors = 0
    
    # Проходим по всем файлам
    for root, dirs, files in os.walk(data_path):
        for file in files:
            local_path = Path(root) / file
            # Относительный путь от bot/data
            relative_path = local_path.relative_to(data_path)
            minio_path = str(relative_path).replace("\\", "/")
            
            # Пропускаем, если уже существует
            if storage_service.file_exists(minio_path):
                continue
            
            # Загружаем файл
            try:
                with open(local_path, "rb") as f:
                    from io import BytesIO
                    file_data = BytesIO(f.read())
                    if storage_service.save_file(minio_path, file_data):
                        uploaded += 1
                        if uploaded % 10 == 0:
                            logger.info(f"Загружено файлов: {uploaded}")
                    else:
                        errors += 1
                        logger.error(f"Ошибка загрузки: {minio_path}")
            except Exception as e:
                errors += 1
                logger.error(f"Ошибка при чтении {local_path}: {e}")
    
    if uploaded > 0:
        logger.info(f"✅ Загружено {uploaded} файлов в MinIO")
    if errors > 0:
        logger.warning(f"⚠️ Ошибок при загрузке: {errors}")

