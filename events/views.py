from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main_app.views import MethodModelViewSet
from main_app import models
from main_app import permissions
from main_app.pagination import TwentyPagination
from main_app.filters import NotNullOrderingFilter, OwnerFilter, DateTimeFilter

from . import serializers


class EventViewSet(MethodModelViewSet):
    queryset = models.Event.objects.all()
    permission_classes = [
        permissions.IsOwner,
        IsAuthenticatedOrReadOnly
    ]
    serializer_class = serializers.EventSerializer
    pagination_class = TwentyPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        NotNullOrderingFilter,
        DateTimeFilter,
        OwnerFilter
    ]
    filterset_fields = ['id', 'title', 'text', 'datetime_end', 'datetime_start']
    search_fields = ['id', 'title', 'text', 'datetime_end', 'datetime_start']
