from drf_spectacular.extensions import OpenApiFilterExtension
from drf_spectacular.openapi import AutoSchema as SpectacularAutoSchema
from rest_framework.generics import RetrieveAPIView


class AutoSchema(SpectacularAutoSchema):
    def _is_retrieve_operation(self):
        if self.method != "GET":
            return False

        if getattr(self.view, "action", None) == "retrieve":
            return True
        if isinstance(self.view, RetrieveAPIView):
            return True

        return False

    def _get_filter_parameters(self):
        if not (self._is_a_general_list_view() or self._is_list_view() or self._is_retrieve_operation()):
            return []
        if getattr(self.view, "filter_backends", None) is None:
            return []

        parameters = []
        for filter_backend in self.view.filter_backends:
            filter_extension = OpenApiFilterExtension.get_match(filter_backend())
            if filter_extension:
                parameters += filter_extension.get_schema_operation_parameters(self)
            else:
                parameters += filter_backend().get_schema_operation_parameters(self.view)
        return parameters

    def _is_a_general_list_view(self):
        return hasattr(self.view, "detail") and self.method.lower() == "get" and not self.view.detail

    def get_response_serializers(self):
        from app.base.views import AbsViewSet

        """ override this for custom behaviour """
        if isinstance(self.view, AbsViewSet):
            actions_serializer = self.view.action
            if self.view.action_serializers.get(f"{actions_serializer}_display"):
                return self.view.action_serializers[f"{actions_serializer}_display"]()
        return super().get_response_serializers()
