from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework import permissions
from app.base.mixins import APIMixin
from app.base.ordering import OrderingFilterWithSchema

__all__ = ["AbsViewSet", "RLViewSet", "LViewSet", "RViewSet", "CLViewSet", "CLUViewSet", "CDLViewSet"]


class AbsViewSet(APIMixin, GenericViewSet):
    filter_backends = (OrderingFilterWithSchema, SearchFilter, DjangoFilterBackend)
    ordering_fields = []
    search_fields = []

    def list_action(self, queryset: QuerySet):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class LViewSet(ListModelMixin, AbsViewSet):
    permission_classes = (permissions.IsAuthenticated,)


class RViewSet(RetrieveModelMixin, AbsViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RLViewSet(ListModelMixin, RViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CLViewSet(CreateModelMixin, LViewSet):
    permission_classes = (permissions.IsAuthenticated,)


class CLUViewSet(UpdateModelMixin, CLViewSet):
    permission_classes = (permissions.IsAuthenticated,)


class CDLViewSet(CreateModelMixin, DestroyModelMixin, LViewSet):
    permission_classes = (permissions.IsAuthenticated,)
