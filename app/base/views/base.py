from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.base.mixins import APIMixin
from app.base.ordering import OrderingFilterWithSchema

__all__ = ["AbsViewSet"]


class AbsViewSet(APIMixin, GenericViewSet):
    filter_backends = (OrderingFilterWithSchema, SearchFilter, DjangoFilterBackend)

    def list_action(self, queryset: QuerySet):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
