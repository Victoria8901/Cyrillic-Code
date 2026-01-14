# 🔧 Исправление ошибки деплоя в Dokploy

## Проблема

Ошибка: `failed to read dockerfile: open .../Dockefile: no such file or directory`

Dokploy ищет файл `Dockefile` (с опечаткой) вместо `Dockerfile`.

## Решение

### Вариант 1: Настройка в UI Dokploy (рекомендуется)

1. Зайдите в настройки проекта в Dokploy
2. Найдите раздел **Build Settings** или **Dockerfile Path**
3. Убедитесь, что указано: `Dockerfile` (не `Dockefile`)
4. Или укажите полный путь: `./Dockerfile`

### Вариант 2: Использование docker-compose

Если Dokploy поддерживает docker-compose:

1. В настройках проекта выберите тип: **Docker Compose**
2. Укажите путь к файлу: `docker-compose.yml`
3. Dokploy автоматически найдет Dockerfile из docker-compose.yml

### Вариант 3: Проверка файлов в репозитории

Убедитесь, что в репозитории есть файл `Dockerfile` (с большой буквы D):

```bash
# Проверьте в репозитории
ls -la Dockerfile
```

Файл должен называться именно `Dockerfile` (без расширения, с большой D).

## Быстрое исправление

1. В Dokploy UI:
   - Settings → Build → Dockerfile Path
   - Установите: `Dockerfile` или `./Dockerfile`

2. Или переключитесь на Docker Compose:
   - Settings → Deploy Type → Docker Compose
   - Compose File: `docker-compose.yml`

3. Сохраните и перезапустите деплой

## Проверка

После исправления деплой должен найти файл:
```
✅ [internal] load build definition from Dockerfile
```

