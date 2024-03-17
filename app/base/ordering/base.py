from rest_framework.filters import OrderingFilter

__all__ = ["OrderingFilterWithSchema"]


class OrderingFilterWithSchema(OrderingFilter):
    @staticmethod
    def _get_description(view):
        all_fields = [
            *getattr(view, "ordering_fields", []),
            *getattr(view, "custom_ordering_fields", []),
        ]
        return ", ".join(all_fields)

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": "ordering",
                "required": False,
                "in": "query",
                "description": self._get_description(view),
                "schema": {
                    "type": "string",
                },
            },
        ]
