# API Testing Project

Проект для тестирования API с использованием FastAPI и pytest. API имитирует сервис ReqRes, предоставляя эндпоинты для работы с пользователями.

## Структура проекта

```
reqres_tests/
├── src/                    # Исходный код API
│   ├── __init__.py
│   ├── api.py             # Основной файл с API эндпоинтами
│   ├── data.py            # Начальные данные
│   └── models/            # Pydantic модели данных
│       ├── __init__.py
│       ├── app_status.py
│       ├── pagination.py
│       └── users.py
├── tests/                  # Тесты
│   ├── __init__.py
│   ├── conftest.py        # Конфигурация pytest
│   ├── test_smoke.py      # Smoke тесты
│   └── test_users.py      # Тесты для API пользователей
├── data.json              # Данные пользователей
├── poetry.lock            # Заблокированные версии зависимостей
├── pyproject.toml         # Зависимости проекта
├── pytest.ini             # Конфигурация pytest
├── run_server.py          # Скрипт запуска сервера
├── start_server.bat       # Батч-файл для Windows
└── README.md              # Документация
```

## API Endpoints

- `GET /api/users` - получить список пользователей с пагинацией
- `GET /api/users/{user_id}` - получить информацию о конкретном пользователе
- `POST /api/users` - создать нового пользователя
- `PUT /api/users/{user_id}` - обновить информацию о пользователе
- `DELETE /api/users/{user_id}` - удалить пользователя

## Установка и запуск

1. Установите Poetry (если еще не установлен):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Установите зависимости:
```bash
poetry install
```

3. Настройте переменные окружения:
```bash
# Скопируйте файл с примером переменных окружения
cp env.sample .env

# Отредактируйте .env при необходимости
```

4. Запустите API сервер:
```bash
poetry run python app/main.py
```

5. В другом терминале запустите тесты:
```bash
poetry run pytest
```

## Переменные окружения

Проект использует следующие переменные окружения (определены в `.env`):

- `BASE_URL` - базовый URL для API (по умолчанию: http://localhost:8002)
- `DATABASE_ENGINE` - строка подключения к базе данных PostgreSQL
- `DATABASE_POOL_SIZE` - размер пула соединений с базой данных (по умолчанию: 10)

Переменные PostgreSQL (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST_AUTH_METHOD) определяются в `docker-compose.yml` и не требуют настройки в `.env`.

## Тесты

Проект содержит параметризированные тесты для всех эндпоинтов API:
- Тестирование получения информации о разных пользователях
- Тестирование создания пользователей с разными данными
- Тестирование обновления информации о пользователях
- Тестирование удаления пользователей
- Тестирование пагинации списка пользователей

 ## Линтинг и форматирование

Проект использует **ruff** для линтинга и форматирования кода.

### Основные команды ruff:

```bash
# Проверка всего проекта на ошибки
poetry run ruff check .

# Автоматическое исправление ошибок
poetry run ruff check . --fix

# Форматирование кода
poetry run ruff format .

# Проверка конкретной папки
poetry run ruff check app/
poetry run ruff check tests/

# Проверка конкретного файла
poetry run ruff check app/main.py

# Проверка с показом всех исправлений
poetry run ruff check . --show-fixes

# Проверка с показом статистики
poetry run ruff check . --statistics
```

### Полезные команды:

```bash
# Показать все доступные правила
poetry run ruff rule --all

# Показать информацию о конкретном правиле
poetry run ruff rule E501

# Проверка с игнорированием конкретных правил
poetry run ruff check . --ignore E501,W503

# Проверка только с определенными правилами
poetry run ruff check . --select E,W,F

# Проверка с автоисправлением и форматированием
poetry run ruff check . --fix && poetry run ruff format .
```

### Примеры использования:

```bash
# Ежедневная проверка проекта
poetry run ruff check . --fix
poetry run ruff format .

# Перед коммитом
poetry run ruff check app/ tests/ --fix
poetry run ruff format app/ tests/

# Проверка только тестов
poetry run ruff check tests/ --fix
```

## Технологии

- FastAPI - фреймворк для создания API
- Pydantic - валидация данных
- pytest - фреймворк для тестирования
- Poetry - управление зависимостями
- ruff - линтинг и форматирование кода 