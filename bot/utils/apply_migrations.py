"""Скрипт для применения миграций БД"""
import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import psycopg2
from config import settings

def apply_migrations():
    """Применить миграции к базе данных"""
    db_config = settings.db
    
    try:
        # Подключаемся к БД
        conn = psycopg2.connect(
            host=db_config.host,
            port=db_config.port,
            database=db_config.database,
            user=db_config.user,
            password=db_config.password
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Читаем файл миграции
        migration_file = project_root / "migrations" / "001_initial_schema.sql"
        
        if not migration_file.exists():
            print(f"❌ Файл миграции не найден: {migration_file}")
            return False
        
        print(f"📄 Читаю миграцию: {migration_file}")
        with open(migration_file, "r", encoding="utf-8") as f:
            migration_sql = f.read()
        
        # Проверяем, существуют ли уже таблицы
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)
        tables_exist = cursor.fetchone()[0]
        
        if tables_exist:
            print("ℹ️  Таблицы уже существуют, пропускаю миграции")
            print("   (Миграции используют IF NOT EXISTS, так что это безопасно)")
        else:
            print("🔄 Применяю миграции...")
        
        # Применяем миграцию (IF NOT EXISTS делает это безопасным)
        cursor.execute(migration_sql)
        
        print("✅ Миграции проверены/применены!")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        print(f"   Проверьте настройки: {db_config.host}:{db_config.port}/{db_config.database}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при применении миграций: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Применение миграций БД...\n")
    success = apply_migrations()
    sys.exit(0 if success else 1)

