from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import FieldError
from django.db.models import F
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import status

"""
 В этом файле содержатся родительские классы viewsets с расширенным спектром возможностей
"""


# Родительский класс хранящий методы необходимые
# для общей группы обьектов
class MethodModelViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Принудительная фильтрация для всех методов
    # Необходима для работы фильтрации в родительских классах
    def filter_queryset(self, queryset):
        filter_backends = self.filter_backends
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(
                self.request,
                queryset,
                view=self
            )
        return queryset

    # Забирает нужные имена выводимых полей из запроса
    # Выводимый набор полей равен списку переданному в заросе
    def get_list_field_values(self, request):
        flds = request.query_params.get('values', None)
        if flds:
            flds =  flds.strip().strip(' ').split(',')
        else:
            try:
                lst = getattr(self, 'default_list_fields')
            except AttributeError:
                fieldlist = [field.name for field in
                self.serializer_class.Meta.model._meta.fields]
                self.default_list_fields = fieldlist
        self.list_fields = flds if flds else self.default_list_fields

    # Выводит список обьектов с пагинацией
    # Набор полей берет из параметра в очернем классе, либо из запроса
    # если такой есть
    def list(self, request):
        fields_sign = self.get_list_field_values(request)
        queryset = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page,
            many = True,
            fields = self.list_fields
        )
        return self.get_paginated_response(serializer.data)
