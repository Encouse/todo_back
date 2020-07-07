web: gunicorn todo_api.wsgi
worker: celery -A main_app.tasks worker -B --loglevel=info
