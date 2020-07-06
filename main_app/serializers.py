from rest_framework import serializers
from collections import OrderedDict
from django.core import exceptions


'''
Класс для создания подклассов serializer с динамическим набором полей
Как вещественных (сохраняемых, так и)
'''
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
     Сериализатор с динамическим набором полей для вывода
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    # По умолчанию - если обьект существует, не даст создать его опять
    def create(self, validated_data):
        return self.get_first_or_create(model = self.Meta.model, data = validated_data)

    # Обновить поля
    def update(self, instance, validated_data):
        fields = self.Meta.model._meta.fields
        for field in fields:
            attr = validated_data.get(field.name, None)
            if attr:
                setattr(instance, field.name, attr)
        return instance


    # Взять значение из бд, если нет создать, если возвращено больше одного - взять первое
    def get_first_or_create(self, model = None, data = None, **kwargs):
        model = self.Meta.model if not model else model
        try:
            getter_data = kwargs.pop('getter_data', None)
            if getter_data:
                obj = model.objects.get(**getter_data)
            else:
                obj = model.objects.get(**data)
        except exceptions.ObjectDoesNotExist as e:
            obj = model.objects.create(**data)
        except exceptions.MultipleObjectsReturned:
            obj = model.objects.filter(**data)[0]
        assert obj
        return obj if obj else None
