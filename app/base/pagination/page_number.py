from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination

__all__ = ["PageNumberPagination"]


class PageNumberPagination(BasePageNumberPagination):
    def get_next_link(self):
        if not self.page.has_next():
            return None
        next_page = self.page.next_page_number()
        if self.page.number == next_page:
            return None
        return next_page

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        previous_page = self.page.previous_page_number()
        if self.page.number == previous_page:
            return None
        return previous_page
