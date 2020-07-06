from django.db import models
from django.contrib.auth.models import User

# Модель описывает событие (встреча, звонок и т.п.)
class Event(models.Model):
    # Юзер может создавать много событий
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'events'
    )
    title = models.CharField(
        max_length = 250
    )
    text = models.CharField(
        max_length = 3000
    )
    datetime_start = models.DateTimeField(
        auto_now = True
    )
    datetime_end = models.DateTimeField(

    )
