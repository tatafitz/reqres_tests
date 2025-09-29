# Docker Commands Guide

## Основные команды Docker

### Работа с контейнерами
```bash
# Посмотреть запущенные контейнеры
docker ps

# Посмотреть все контейнеры (включая остановленные)
docker ps -a

# Остановить контейнер
docker stop <container_name>

# Удалить контейнер
docker rm <container_name>

# Посмотреть логи контейнера
docker logs <container_name>

# Войти в контейнер
docker exec -it <container_name> /bin/bash
```

### Работа с образами
```bash
# Посмотреть все образы
docker images

# Удалить образ
docker rmi <image_name>

# Удалить все неиспользуемые образы
docker image prune -f

# Удалить все неиспользуемые ресурсы
docker system prune -f
```

## Docker Compose

### Основные команды
```bash
# Запустить все сервисы
docker compose up -d

# Остановить все сервисы
docker compose down

# Посмотреть статус сервисов
docker compose ps

# Посмотреть логи всех сервисов
docker compose logs

# Посмотреть логи конкретного сервиса
docker compose logs <service_name>
```

### Пересборка и перезапуск
```bash
# Пересобрать и запустить все сервисы
docker compose up -d --build

# Пересобрать и запустить конкретный сервис
docker compose up -d --build <service_name>

# Перезапустить конкретный сервис
docker compose restart <service_name>

# Перезапустить все сервисы
docker compose restart
```

## Как избежать лишних образов

### 1. Очистка неиспользуемых образов
```bash
# Удалить все неиспользуемые образы
docker image prune -f

# Удалить все неиспользуемые ресурсы
docker system prune -f

# Удалить все неиспользуемые ресурсы включая volumes
docker system prune -af --volumes
```

### 2. Использование тегов
```bash
# Собрать образ с тегом
docker build -t myapp:latest .

# Собрать образ с версией
docker build -t myapp:v1.0 .
```

### 3. Многоэтапная сборка
```dockerfile
# В Dockerfile используйте многоэтапную сборку
FROM python:3.11 as builder
# ... этап сборки

FROM python:3.11-slim as runtime
# ... финальный этап
```

### Пересборка и запуск приложения
```bash
# Остановить все сервисы
docker compose down

# Пересобрать и запустить все сервисы
docker compose up -d --build

# Или только приложение
docker compose up -d --build app
```

### Проверка статуса
```bash
# Статус всех сервисов
docker compose ps

# Логи приложения
docker compose logs app

# Логи в реальном времени
docker compose logs -f app
```

### Очистка
```bash
# Удалить неиспользуемые образы
docker image prune -f

# Удалить все неиспользуемые ресурсы
docker system prune -f
```

## Полезные команды для отладки

```bash
# Войти в контейнер приложения
docker compose exec app /bin/bash

# Проверить переменные окружения в контейнере
docker compose exec app env

# Проверить процессы в контейнере
docker compose exec app ps aux

# Проверить сетевые соединения
docker compose exec app netstat -tlnp
```

## Рекомендации

1. Используйте `docker compose` вместо отдельных `docker run`
2. Регулярно очищайте неиспользуемые образы
3. Используйте `.dockerignore` для исключения ненужных файлов
4. Используйте многоэтапную сборку для уменьшения размера образов
5. Используйте теги для версионирования образов

## Частые проблемы и решения

### Проблема: Контейнер не пересобирается
```bash
# Решение: Принудительная пересборка без кэша
docker compose build --no-cache
docker compose up -d
```

### Проблема: Порт уже используется
```bash
# Решение: Остановить все контейнеры и перезапустить
docker compose down
docker compose up -d
```

### Проблема: Много неиспользуемых образов
```bash
# Решение: Очистка
docker system prune -af
```

### Проблема: Контейнер не запускается
```bash
# Решение: Проверить логи
docker compose logs <service_name>

# Или логи конкретного контейнера
docker logs <container_name>
```
