from fastapi import FastAPI, HTTPException
from celery.result import AsyncResult
import redis
import json
from tasks import calculate_task, calculate_new
from celery_app import celery_app

app = FastAPI(title="Simple Celery API")


@app.post("/start_calculation/{number}")
async def start_calculation(number: int):
    """Запуск фонового расчета"""
    task = calculate_task.delay(number)
    return {
        "task_id": task.id,
        "message": "Расчет запущен",
        "number": number
    }

@app.post("/start_calculation_2/{number}")
async def start_calculation_2(number: int):
    """Запуск фонового расчета"""
    task = calculate_new.delay(number)
    return {
        "task_id": task.id,
        "message": "Расчет запущен",
        "number": number
    }


@app.get("/task_status/{task_id}")
async def get_task_status(task_id: str):
    """Получение статуса конкретной задачи"""
    task_result = AsyncResult(task_id)

    # Если задача завершена успешно
    if task_result.successful():
        return {
            "task_id": task_id,
            "status": "SUCCESS",
            "result": task_result.result,
            "complete": True
        }

    # Если задача завершена с ошибкой
    elif task_result.failed():
        return {
            "task_id": task_id,
            "status": "FAILURE",
            "error": str(task_result.result),
            "complete": True
        }

    # Если задача еще выполняется
    else:
        return {
            "task_id": task_id,
            "status": task_result.status,
            "complete": False
        }


@app.get("/all_tasks")
async def get_all_tasks():
    """Показать все задачи из Redis"""
    try:
        # Подключаемся к Redis
        r = redis.Redis(host='localhost', port=6379, db=0)

        # Ищем все ключи с результатами задач
        task_keys = r.keys('celery-task-meta-*')

        tasks = []
        for key in task_keys:
            task_id = key.decode().replace('celery-task-meta-', '')
            task_data = r.get(key)

            if task_data:
                task_info = json.loads(task_data)
                tasks.append({
                    "task_id": task_id,
                    "status": task_info.get('status', 'UNKNOWN'),
                    "result": task_info.get('result', {}),
                    "date_done": task_info.get('date_done')
                })

        # Сортируем по дате (новые сверху)
        tasks.sort(key=lambda x: x.get('date_done') or '', reverse=True)

        return {
            "total_tasks": len(tasks),
            "tasks": tasks
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "ok", "message": "Service is running"}