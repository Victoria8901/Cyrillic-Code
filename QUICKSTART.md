# 🚀 Быстрый старт

## 1. Настройка

Создайте файл `.env` из примера:
```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите токен бота:
```env
BOT_TOKEN=ваш_токен_от_BotFather
```

## 2. Запуск через Docker Compose (рекомендуется)

```bash
# Запустить все сервисы
docker-compose up -d

# Посмотреть логи бота
docker-compose logs -f bot

# Остановить
docker-compose down
```

## 3. Запуск локально (для разработки)

### Требования:
- Python 3.13+
- PostgreSQL (можно через Docker: `docker-compose up -d postgres`)

### Установка:
```bash
# Установить зависимости
pip install -r requirements.txt

# Применить миграции БД
psql -h localhost -U bot_user -d oge_ege_bot -f migrations/001_initial_schema.sql
```

### Запуск:
```bash
python -m bot.main
```

## 4. Проверка работы

Найдите бота в Telegram и отправьте `/start`

## ⚙️ Дополнительные настройки

### Хранение файлов

**По умолчанию файлы хранятся в MinIO** (объектное хранилище). При первом запуске бот автоматически загрузит все файлы из `bot/data/` в MinIO.

Если нужно использовать локальное хранение, установите в `.env`:
```env
USE_MINIO=false
```

Для ручной загрузки файлов в MinIO:
```bash
docker-compose exec bot python -m bot.utils.upload_to_minio
```

## 📝 Основные команды Docker

```bash
# Запустить
docker-compose up -d

# Остановить
docker-compose down

# Перезапустить
docker-compose restart bot

# Логи
docker-compose logs -f bot

# Войти в контейнер
docker-compose exec bot bash
```

## ❗ Важно

- Убедитесь, что `BOT_TOKEN` указан в `.env`
- При первом запуске БД автоматически инициализируется
- Файлы заданий должны быть в `bot/data/OGE/`

