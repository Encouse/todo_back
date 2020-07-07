from celery import Celery
from django.core.mail import send_mail
import time
from datetime import datetime
import os
import redis

r = redis.from_url(os.environ.get("REDIS_URL"))

app = Celery('tasks', broker='pyamqp://guest@localhost//')
app.conf.update(BROKER_URL=r,
                CELERY_RESULT_BACKEND=r,)


@app.task
def send_event_mail(event):
    end_date = time.mktime(datetime.timetuple(event.datetime_end))
    date_now = time.time()
    predict = 60*60
    wait_for = end_date - date_now - predict
    time.sleep(wait_for)
    email = event.user.email
    send_mail(
        f'Событие {event.title}',
        f'Ваше событие {event.title} начнется через 60 минут!',
        'eventstestserver@gmail.com',
        [email],
        fail_silently=False,
    )
