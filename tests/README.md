# Структура тестов

Тесты организованы по функциональным областям для лучшей читаемости и поддержки.

## Модули тестирования

### `test_smoke.py` 
**Smoke тесты** - базовые тесты работоспособности
- `test_server_available` - проверка доступности сервера
- `test_status` - проверка эндпоинта статуса

### `test_users.py`
**Тесты пользователей** - основная функциональность работы с пользователями
- `test_get_single_user` - получение информации о пользователе
- `test_get_single_user_not_found` - тест 404 ошибки
- `test_get_single_user_negative_or_zero_id` - тест невалидных ID (числовые)
- `test_get_single_user_string_id` - тест невалидных ID (строковые)
- `test_users_no_duplicates` - проверка отсутствия дубликатов
- `test_create_user` - создание пользователя
- `test_update_user` - обновление пользователя
- `test_delete_user` - удаление пользователя

### `test_pagination.py`
**Тесты пагинации** - проверка системы пагинации

#### `TestPagination` - Основные тесты пагинации
- `test_pagination_metadata_and_items_count` - проверка page, size, total, pages и количества элементов
- `test_pages_calculation_different_sizes` - проверка pages при разных size
- `test_different_pages_return_different_data` - проверка разных данных при разных page
- `test_last_page_partial_fill` - тест остатка на последней странице
- `test_empty_page_beyond_last` - тест страницы за пределами последней

## Принципы тестирования

### ✅ Что мы делаем правильно:
1. **Отсутствие if-statements в тестах** - каждый тест проверяет одну конкретную ситуацию
2. **Динамические тестовые данные** - тесты рассчитывают ожидаемые значения на основе реальных данных
3. **Четкое разделение ответственности** - каждый тест имеет одну конкретную цель
4. **Параметризация** - эффективное покрытие различных сценариев
5. **Типизация** - все функции имеют аннотации типов

### 🚫 Чего мы избегаем:
1. **If-statements в тестах** - вместо них создаем отдельные тесты
2. **Захардкоженные значения** - используем динамические расчеты
3. **Монолитные тесты** - разбиваем на логические части
4. **Смешение ответственности** - один тест = одна проверка

## Запуск тестов

```bash
# Все тесты
poetry run pytest

# Конкретный модуль
poetry run pytest tests/test_pagination.py

# Конкретный класс
poetry run pytest tests/test_pagination.py::TestPagination

# Конкретный тест
poetry run pytest tests/test_pagination.py::TestPagination::test_pagination_metadata_and_items_count
```

## Fixtures

### `base_url`
Базовый URL для API тестов (из переменных окружения)

### `total_users` (в test_pagination.py)
Динамическое получение общего количества пользователей для расчетов пагинации

### `users` (в conftest.py)
Получение списка пользователей через API