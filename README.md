# Бот для подготовки к ОГЭ и ЕГЭ по русскому языку

Telegram-бот для подготовки к ОГЭ и ЕГЭ по русскому языку. Бот помогает пользователям изучать теорию, решать задания и проходить тесты.

## 🚀 Возможности

- 📚 Подготовка к ОГЭ (задания 2-9)
- 📖 Подготовка к ЕГЭ (задания 4-21) - в разработке
- 📊 Отслеживание прогресса пользователя
- ✅ Автоматическая проверка ответов
- 🧪 Тестирование после изучения темы
- 📁 Хранение файлов в объектном хранилище (MinIO) или локально

## 📋 Требования

- Docker и Docker Compose
- Python 3.13+ (для локальной разработки)
- PostgreSQL 16+
- Redis (опционально)
- MinIO (опционально, для объектного хранилища)

## 🛠️ Установка и запуск

> 💡 **Быстрый старт**: Смотрите [QUICKSTART.md](QUICKSTART.md) для краткой инструкции
> 
> 🚀 **Деплой в Dokploy**: Смотрите [DEPLOY.md](DEPLOY.md) для инструкции по деплою через SSH Git

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd Cyrillic-Code
```

### 2. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env` и заполните необходимые значения:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
# Bot Configuration
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=oge_ege_bot
DB_USER=bot_user
DB_PASSWORD=bot_password

# Redis Configuration (опционально)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# MinIO Configuration
# По умолчанию MinIO включен. Установите USE_MINIO=false для локального хранения
USE_MINIO=true
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=oge-ege-files
MINIO_USE_SSL=false
USE_MINIO=false
```

### 3. Запуск с Docker Compose

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL базу данных
- Redis (опционально)
- MinIO объектное хранилище (по умолчанию включено)
- Telegram бота

**При первом запуске** бот автоматически загрузит все файлы из `bot/data/` в MinIO.

### 4. Проверка работы

Проверьте логи бота:

```bash
docker-compose logs -f bot
```

## 📁 Структура проекта

```
.
├── bot/                    # Основной код бота
│   ├── handlers/          # Обработчики сообщений
│   ├── keyboards/          # Клавиатуры
│   ├── models/             # Модели данных и FSM состояния
│   ├── services/           # Бизнес-логика
│   ├── data/               # Данные (задания, теория)
│   └── main.py            # Точка входа
├── config/                 # Конфигурация
├── migrations/             # SQL миграции
├── docker-compose.yml      # Docker Compose конфигурация
├── Dockerfile              # Docker образ бота
├── requirements.txt        # Python зависимости
└── README.md              # Документация
```

## 💾 Хранение данных

### База данных
База данных PostgreSQL автоматически инициализируется при первом запуске через миграции в папке `migrations/`. Данные БД хранятся в Docker volume `postgres_data`.

### Файлы (задания и теория)

**По умолчанию файлы хранятся в MinIO** (объектное хранилище). При первом запуске бот автоматически загрузит все файлы из `bot/data/` в MinIO.

**Преимущества MinIO (по умолчанию):**
- ✅ Масштабируемость
- ✅ Резервное копирование
- ✅ Доступ из нескольких инстансов
- ✅ S3-совместимое API
- ✅ Автоматическая загрузка при первом запуске

**Локальное хранение (опционально):**

Если нужно использовать локальное хранение, установите в `.env`:
```env
USE_MINIO=false
```

Для ручной загрузки файлов в MinIO (если нужно):
```bash
docker-compose exec bot python -m bot.utils.upload_to_minio
```

### Основные таблицы:

- `users` - пользователи бота
- `oge_topics` - темы ОГЭ
- `ege_topics` - темы ЕГЭ
- `user_oge_progress` - прогресс пользователей по ОГЭ
- `user_ege_progress` - прогресс пользователей по ЕГЭ
- `oge_tasks` - задания ОГЭ (для будущего использования)
- `ege_tasks` - задания ЕГЭ (для будущего использования)
- `task_attempts` - история попыток решения заданий

## 🔧 Разработка

### Локальная разработка

1. Установите зависимости:

```bash
pip install -r requirements.txt
```

2. Запустите PostgreSQL локально или используйте Docker:

```bash
docker-compose up -d postgres
```

3. Примените миграции:

```bash
psql -h localhost -U bot_user -d oge_ege_bot -f migrations/001_initial_schema.sql
```

4. Запустите бота:

```bash
python -m bot.main
```

### Добавление заданий

Задания хранятся в папке `bot/data/OGE/task{N}/` в формате:
- `{id}.txt` - файлы с заданиями (формат: текст задания + "Ответ:" + правильный ответ)
- `task_{N}_theory.pdf` - файл с теорией

## 📝 Использование

1. Найдите бота в Telegram
2. Отправьте команду `/start`
3. Выберите "Подготовка к ОГЭ" или "Подготовка к ЕГЭ"
4. Выберите номер задания
5. Изучите теорию
6. Решайте задания (после 10 правильных ответов будет предложен тест)
7. Пройдите тест (нужно набрать минимум 80% правильных ответов)

## 🐛 Устранение неполадок

### Бот не запускается

1. Проверьте, что `BOT_TOKEN` установлен в `.env`
2. Проверьте логи: `docker-compose logs bot`
3. Убедитесь, что база данных запущена: `docker-compose ps`

### Ошибки подключения к БД

1. Проверьте настройки в `.env`
2. Убедитесь, что PostgreSQL запущен: `docker-compose ps postgres`
3. Проверьте логи PostgreSQL: `docker-compose logs postgres`

## 📄 Лицензия

[Укажите лицензию]

## 👥 Авторы

[Укажите авторов]

## 🔗 Ссылки

- [Aiogram документация](https://docs.aiogram.dev/)
- [PostgreSQL документация](https://www.postgresql.org/docs/)
- [MinIO документация](https://min.io/docs/)

