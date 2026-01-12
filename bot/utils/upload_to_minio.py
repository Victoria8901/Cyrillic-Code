"""Скрипт для загрузки файлов в MinIO"""
import os
import sys
from pathlib import Path
from io import BytesIO

# Добавляем корневую директорию в путь для импорта
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from bot.services.storage import storage_service

def upload_files_to_minio():
    """Загрузить все файлы из bot/data в MinIO"""
    if not storage_service.use_minio:
        print("❌ MinIO не включен. Установите USE_MINIO=true в .env")
        return
    
    data_path = Path("bot/data")
    if not data_path.exists():
        print(f"❌ Директория {data_path} не найдена")
        return
    
    uploaded = 0
    skipped = 0
    errors = 0
    
    # Проходим по всем файлам
    for root, dirs, files in os.walk(data_path):
        for file in files:
            local_path = Path(root) / file
            # Относительный путь от bot/data
            relative_path = local_path.relative_to(data_path)
            minio_path = str(relative_path).replace("\\", "/")
            
            # Проверяем, существует ли файл в MinIO
            if storage_service.file_exists(minio_path):
                print(f"⏭️  Пропущен (уже существует): {minio_path}")
                skipped += 1
                continue
            
            # Загружаем файл
            try:
                with open(local_path, "rb") as f:
                    file_data = BytesIO(f.read())
                    if storage_service.save_file(minio_path, file_data):
                        print(f"✅ Загружен: {minio_path}")
                        uploaded += 1
                    else:
                        print(f"❌ Ошибка загрузки: {minio_path}")
                        errors += 1
            except Exception as e:
                print(f"❌ Ошибка при чтении {local_path}: {e}")
                errors += 1
    
    print(f"\n📊 Итого:")
    print(f"   ✅ Загружено: {uploaded}")
    print(f"   ⏭️  Пропущено: {skipped}")
    print(f"   ❌ Ошибок: {errors}")


if __name__ == "__main__":
    print("🚀 Начинаем загрузку файлов в MinIO...\n")
    upload_files_to_minio()

