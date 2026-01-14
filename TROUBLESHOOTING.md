# 🔧 Устранение проблем

## Проблема 1: MinIO не подключается

**Ошибка:**
```
Failed to initialize MinIO: HTTPConnectionPool(host='localhost', port=9000): Connection refused
```

**Причина:** MinIO пытается подключиться к `localhost:9000`, но в Docker Compose MinIO доступен по имени сервиса `minio:9000`.

**Решение:**

В Dokploy в переменных окружения установите:
```env
MINIO_ENDPOINT=minio:9000
```

Или если используете внешний MinIO:
```env
MINIO_ENDPOINT=ваш_хост:9000
```

**Проверка:**
```bash
# В контейнере бота
docker-compose exec bot env | grep MINIO
```

## Проблема 2: База данных не инициализирована

**Ошибка:**
```
Database error: relation "users" does not exist
```

**Причина:** Миграции не были применены к базе данных.

**Решение:**

### Вариант 1: Автоматическое применение (рекомендуется)

Бот автоматически применит миграции при запуске. Если это не сработало:

### Вариант 2: Ручное применение

```bash
# В контейнере бота
docker-compose exec bot python -m bot.utils.apply_migrations

# Или локально (если БД доступна)
python -m bot.utils.apply_migrations
```

### Вариант 3: Через psql

```bash
# Подключиться к PostgreSQL
docker-compose exec postgres psql -U bot_user -d oge_ege_bot

# Или если БД на другом сервере
psql -h ваш_хост -U bot_user -d oge_ege_bot -f migrations/001_initial_schema.sql
```

### Вариант 4: Пересоздать volume PostgreSQL

⚠️ **ВНИМАНИЕ: Это удалит все данные!**

```bash
docker-compose down -v  # Удаляет volumes
docker-compose up -d    # Создает заново с миграциями
```

## Проблема 3: Telegram Conflict

**Ошибка:**
```
TelegramConflictError: terminated by other getUpdates request; 
make sure that only one bot instance is running
```

**Причина:** Запущено несколько экземпляров бота одновременно с одним токеном.

**Решение:**

1. **Остановите все экземпляры бота:**
   ```bash
   # В Dokploy - остановите все деплои этого бота
   # Или локально:
   docker-compose stop bot
   docker ps | grep bot  # Проверьте, нет ли других контейнеров
   ```

2. **Проверьте процессы:**
   ```bash
   ps aux | grep "bot.main"  # Найдите запущенные процессы
   kill <PID>  # Остановите лишние
   ```

3. **Запустите только один экземпляр:**
   ```bash
   docker-compose up -d bot
   ```

## Проблема 4: Переменные окружения не установлены

**Симптомы:** Бот не может подключиться к сервисам.

**Решение:**

Проверьте все переменные окружения в Dokploy:

**Обязательные:**
- `BOT_TOKEN` - токен бота от BotFather
- `DB_HOST` - хост PostgreSQL (в docker-compose: `postgres`)
- `DB_USER` - пользователь БД
- `DB_PASSWORD` - пароль БД
- `DB_NAME` - имя БД

**Для MinIO:**
- `MINIO_ENDPOINT` - в docker-compose: `minio:9000`
- `MINIO_ACCESS_KEY` - ключ доступа
- `MINIO_SECRET_KEY` - секретный ключ

**Проверка:**
```bash
docker-compose exec bot env | grep -E "BOT_TOKEN|DB_|MINIO_"
```

## Проблема 5: Файлы не загружаются в MinIO

**Симптомы:** Бот работает, но задания не загружаются.

**Решение:**

1. **Проверьте, что MinIO запущен:**
   ```bash
   docker-compose ps minio
   ```

2. **Проверьте логи MinIO:**
   ```bash
   docker-compose logs minio
   ```

3. **Загрузите файлы вручную:**
   ```bash
   docker-compose exec bot python -m bot.utils.upload_to_minio
   ```

4. **Проверьте доступность MinIO:**
   ```bash
   docker-compose exec bot curl http://minio:9000/minio/health/live
   ```

## Проблема 6: Бот не отвечает

**Диагностика:**

1. **Проверьте логи:**
   ```bash
   docker-compose logs -f bot
   ```

2. **Проверьте статус контейнера:**
   ```bash
   docker-compose ps
   ```

3. **Проверьте подключение к БД:**
   ```bash
   docker-compose exec bot python -c "from bot.services.database import db_service; print(db_service.get_connection())"
   ```

4. **Проверьте токен бота:**
   - Убедитесь, что `BOT_TOKEN` правильный
   - Проверьте в BotFather, что бот активен

## Быстрая проверка всех сервисов

```bash
# Проверка всех контейнеров
docker-compose ps

# Проверка логов всех сервисов
docker-compose logs --tail=50

# Перезапуск всех сервисов
docker-compose restart

# Полная перезагрузка (с пересборкой)
docker-compose up -d --build
```

## Полезные команды

```bash
# Войти в контейнер бота
docker-compose exec bot bash

# Проверить переменные окружения
docker-compose exec bot env

# Проверить подключение к PostgreSQL
docker-compose exec bot psql -h postgres -U bot_user -d oge_ege_bot -c "SELECT 1;"

# Проверить подключение к MinIO
docker-compose exec bot curl http://minio:9000/minio/health/live
```

