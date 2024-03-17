from collections import OrderedDict

from rest_framework.response import Response

from .page_number import PageNumberPagination

__all__ = ["DefaultPageNumberPagination"]


class DefaultPageNumberPagination(PageNumberPagination):
    max_page_size = 30
    page_size = 20

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("current", self.page.number),
                    ("next", self.get_next_link()),
                    ("previews", self.get_previous_link()),
                    ("total", self.page.paginator.num_pages),
                    ("results", data),
                ]
            )
        )
