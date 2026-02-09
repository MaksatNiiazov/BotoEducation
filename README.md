# Сервис сокращения URL

Минимальный production-ориентированный сокращатель ссылок на FastAPI и SQLite (stdlib).

## Требования

- Python 3.12+
- SQLite (входит в Python)

## Установка

Создайте виртуальное окружение и установите зависимости:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
```

## Конфигурация

Все настройки задаются только через переменные окружения:

- `APP_HOST`
- `APP_PORT`
- `DATABASE_PATH`
- `BASE_URL`
- `LOG_LEVEL`

Пример для PowerShell:

```powershell
$env:APP_HOST="127.0.0.1"
$env:APP_PORT="8000"
$env:DATABASE_PATH="D:\Projects\TestTasks\Boto Education\data\links.db"
$env:BASE_URL="http://127.0.0.1:8000"
$env:LOG_LEVEL="INFO"
```

## Запуск приложения

```powershell
python run.py
```

## Запуск тестов

```powershell
python -m pytest
```

## Запуск через Docker

Сборка образа:

```powershell
docker build -t url-shortener .
```

Запуск контейнера (пример для PowerShell):

```powershell
$env:APP_HOST="0.0.0.0"
$env:APP_PORT="8000"
$env:DATABASE_PATH="/data/links.db"
$env:BASE_URL="http://localhost:8000"
$env:LOG_LEVEL="INFO"
docker run --rm -p 8000:8000 -e APP_HOST -e APP_PORT -e DATABASE_PATH -e BASE_URL -e LOG_LEVEL -v "${PWD}\data:/data" url-shortener
```

## Примеры API запросов

Создать короткую ссылку:

```bash
curl -X POST http://127.0.0.1:8000/shorten -H "Content-Type: application/json" -d '{"url":"https://example.com/very/long/link"}'
```

Редирект:

```bash
curl -i http://127.0.0.1:8000/abc123
```
