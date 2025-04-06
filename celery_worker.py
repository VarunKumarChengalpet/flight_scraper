from celery import Celery

celery_app = Celery(
    "flight_scraper",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Route this task to the 'scraper' queue
celery_app.conf.task_routes = {
    "tasks.flight_tasks.scrape_flight_info_task": {"queue": "scraper"},
}

import tasks.flight_tasks
