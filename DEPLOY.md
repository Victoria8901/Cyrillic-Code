# 🚀 Деплой в Dokploy

Инструкция по деплою бота в Dokploy через SSH Git.

## 📋 Подготовка

### 1. Убедитесь, что в репозитории есть:

- ✅ `Dockerfile` - для сборки образа бота
- ✅ `docker-compose.yml` - для оркестрации сервисов
- ✅ `.env.example` - пример переменных окружения
- ✅ `requirements.txt` - зависимости Python
- ✅ Все файлы заданий в `bot/data/`

### 2. Настройка в Dokploy

#### Шаг 1: Создание проекта

1. Войдите в Dokploy
2. Создайте новый проект
3. Выберите тип: **Docker Compose** или **Docker**

#### Шаг 2: Подключение Git репозитория

1. Выберите **Git Repository**
2. Укажите URL вашего репозитория (SSH)
3. Настройте SSH ключ в Dokploy (если нужно)
4. Выберите ветку (обычно `main` или `master`)

#### Шаг 3: Настройка переменных окружения

В разделе **Environment Variables** добавьте все переменные из `.env.example`:

**Обязательные:**
```env
BOT_TOKEN=ваш_токен_от_BotFather
```

**База данных:**
```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=oge_ege_bot
DB_USER=bot_user
DB_PASSWORD=надежный_пароль
```

**MinIO:**
```env
USE_MINIO=true
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=надежный_пароль
MINIO_BUCKET=oge-ege-files
MINIO_USE_SSL=false
```

**Опционально:**
```env
ADMIN_IDS=123456789,987654321
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
```

#### Шаг 4: Настройка сборки

**⚠️ ВАЖНО: Проверьте имя файла!**

Если используете **Docker Compose**:
- Dokploy автоматически найдет `docker-compose.yml`
- Убедитесь, что путь к файлу: `./docker-compose.yml`
- **Рекомендуется**: Используйте Docker Compose для полного стека

Если используете только **Docker**:
- Dokploy найдет `Dockerfile` в корне
- **Убедитесь, что в настройках указано именно `Dockerfile` (не `Dockefile`!)**
- Путь: `Dockerfile` или `./Dockerfile`

**Если видите ошибку "Dockefile":**
1. Зайдите в Settings → Build → Dockerfile Path
2. Установите: `Dockerfile` (с большой D, без опечатки)
3. Сохраните и перезапустите деплой

#### Шаг 5: Порты и сети

Dokploy автоматически настроит сеть для docker-compose. Убедитесь, что:
- PostgreSQL доступен по имени `postgres`
- MinIO доступен по имени `minio`
- Redis доступен по имени `redis` (если используется)

## 🔧 Варианты деплоя

### Вариант 1: Полный стек (рекомендуется)

Используйте `docker-compose.yml` как есть. Dokploy запустит:
- PostgreSQL
- Redis
- MinIO
- Бот

**Преимущества:**
- Все сервисы в одном месте
- Автоматическая настройка сети
- Простое управление

### Вариант 2: Только бот (внешние сервисы)

Если у вас уже есть PostgreSQL и MinIO на другом сервере:

1. Создайте упрощенный `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  bot:
    build: .
    environment:
      BOT_TOKEN: ${BOT_TOKEN}
      DB_HOST: ${DB_HOST}  # Внешний хост
      DB_PORT: ${DB_PORT}
      # ... остальные переменные
    restart: unless-stopped
```

2. В Dokploy используйте этот файл вместо стандартного

## 📝 Важные моменты

### 1. Файлы заданий

Файлы из `bot/data/` будут автоматически загружены в MinIO при первом запуске бота.

**Убедитесь, что:**
- Все файлы заданий находятся в репозитории
- Путь к файлам: `bot/data/OGE/task{N}/*.txt`
- PDF файлы теории: `bot/data/OGE/task{N}/task_{N}_theory.pdf`

### 2. База данных

При первом запуске PostgreSQL автоматически применит миграции из `migrations/001_initial_schema.sql`.

**Важно:**
- Данные БД будут храниться в Docker volume
- При пересоздании контейнера данные сохранятся (если volume не удален)

### 3. MinIO

MinIO будет доступен по адресу `minio:9000` внутри Docker сети.

**Для доступа извне:**
- Настройте порт в Dokploy (если нужен доступ к консоли MinIO)
- Консоль MinIO: порт 9001

### 4. Логи

Проверяйте логи в Dokploy:
- Логи бота: `docker-compose logs bot`
- Логи всех сервисов: `docker-compose logs`

## 🔄 Процесс деплоя

1. **Push в Git** - Dokploy автоматически обнаружит изменения
2. **Сборка образа** - Dokploy соберет Docker образ из Dockerfile
3. **Запуск сервисов** - Dokploy запустит docker-compose
4. **Инициализация** - Бот загрузит файлы в MinIO (если нужно)
5. **Готово** - Бот работает!

## 🐛 Устранение проблем

### Бот не запускается

1. Проверьте логи в Dokploy
2. Убедитесь, что `BOT_TOKEN` установлен
3. Проверьте подключение к БД: `docker-compose logs postgres`

### Файлы не загружаются в MinIO

1. Проверьте логи бота: `docker-compose logs bot | grep -i minio`
2. Убедитесь, что MinIO запущен: `docker-compose ps minio`
3. Проверьте переменные окружения MinIO

### Ошибки подключения к БД

1. Убедитесь, что PostgreSQL запущен
2. Проверьте переменные `DB_HOST`, `DB_USER`, `DB_PASSWORD`
3. Проверьте, что миграции применены

## 📊 Мониторинг

В Dokploy вы можете:
- Просматривать логи в реальном времени
- Мониторить использование ресурсов
- Управлять переменными окружения
- Перезапускать сервисы

## 🔐 Безопасность

**Важно:**
- ✅ Никогда не коммитьте `.env` файл
- ✅ Используйте сильные пароли для БД и MinIO
- ✅ Ограничьте доступ к MinIO консоли
- ✅ Регулярно обновляйте зависимости

## 📚 Дополнительные ресурсы

- [Документация Dokploy](https://dokploy.com/docs)
- [Docker Compose документация](https://docs.docker.com/compose/)

