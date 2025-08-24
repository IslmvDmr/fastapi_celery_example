from celery_app import celery_app
import time


@celery_app.task(bind=True)
def calculate_task(self, number: int):
    """Долгая задача расчета (5 секунд)"""
    # Имитация долгого расчета
    time.sleep(5)

    # Выполняем расчет
    result = number * number

    # Возвращаем результат - задача автоматически перейдет в SUCCESS
    return {
        'number': number,
        'result': result,
        'status': 'complete'
    }