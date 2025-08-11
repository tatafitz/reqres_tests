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

3. Запустите API сервер:
```bash
# Windows
start_server.bat

# Linux/Mac
poetry run python run_server.py
```

4. В другом терминале запустите тесты:
```bash
poetry run pytest
```

## Тесты

Проект содержит параметризированные тесты для всех эндпоинтов API:
- Тестирование получения информации о разных пользователях
- Тестирование создания пользователей с разными данными
- Тестирование обновления информации о пользователях
- Тестирование удаления пользователей
- Тестирование пагинации списка пользователей

## Технологии

- FastAPI - фреймворк для создания API
- Pydantic - валидация данных
- pytest - фреймворк для тестирования
- Poetry - управление зависимостями 