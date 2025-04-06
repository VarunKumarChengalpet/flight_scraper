#!/bin/bash

echo "🔄 Starting Redis..."
# Uncomment the below line if Redis is installed locally and not already running
# redis-server --daemonize yes

sleep 1

echo "🚀 Starting Celery worker..."
celery -A celery_worker.celery_app worker --loglevel=info -Q scraper &
CELERY_PID=$!

sleep 2

echo "🌐 Starting FastAPI server..."
uvicorn main:app --reload &

wait $CELERY_PID
