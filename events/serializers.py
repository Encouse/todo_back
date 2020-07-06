from rest_framework import serializers
from django.core import exceptions
from main_app import models
from main_app.serializers import DynamicFieldsModelSerializer

class EventSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = models.Event
        fields = '__all__'
