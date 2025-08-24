#  FastAPI Celery Docker

Готовый шаблон для запуска фоновых задач с FastAPI и Celery в Docker.
Сделал для личных целей, для ускорения разработки приложений, где нужны фоновые задачи.

## 🚀 Быстрый старт

1. **Скачайте и запустите**:
```bash
docker-compose up -d --build
```

2. **Откройте в браузере**:
   - API: http://localhost
   - Документация: http://localhost/docs
   - Redis мониторинг: http://localhost:8081

3. **Запустите задачу**:
```bash
curl -X POST "http://localhost/start_calculation/5"
```

## 📦 Что внутри

- **FastAPI** - основное API
- **Celery** - фоновые задачи
- **Redis** - очередь задач
- **Nginx** - веб-сервер
- **Redis Commander** - мониторинг Redis

## 🎯 Как использовать

1. **Запустить задачу**:
   ```bash
   POST /start_calculation/10
   ```

2. **Проверить статус**:
   ```bash
   GET /task_status/{task_id}
   ```

3. **Посмотреть все задачи**:
   ```bash
   GET /all_tasks
   ```

## 🛠 Команды

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f
```

