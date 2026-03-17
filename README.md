# project


### Предварительные требования
- Docker и Docker Compose
- Git

# Запуск
```bash
python -m venv venv
```

# Запустить с Docker Compose:
```bash
docker-compose up --build
```

# Documentation API (Swagger UI)
```http://localhost:8000/docs```

## 🐳 Docker

Сборка и запуск в контейнерах:
```bash
# Сборка образов
docker-compose build

# Запуск в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## 🗄 Структура БД

Основные таблицы:
- `payments` - платежи
- `invoices` - счета
- `orders` - заказы
- `clients` - клиенты
- `comments` - отзывы




