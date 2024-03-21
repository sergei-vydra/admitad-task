from rest_framework.settings import api_settings

__all__ = ["APIMixin"]


class APIMixin:
    permission_classes = ()
    auth_classes = ()
    throttle_classes = ()
    action_auth = {}
    action_permissions = {}
    action_serializers = {}
    action_throttle = {}
    action_queryset = {}
    _action_glossary = {
        "list": "list",
        "retrieve": "list",
        "update": "update",
        "partial_update": "update",
        "PATCH": "update",
    }

    @property
    def _action(self):
        return getattr(self, "action", getattr(self.request, "method", None))

    @property
    def authentication_classes(self):
        auth_classes = self.action_auth.get(self._action)
        if not auth_classes:
            auth_classes = self.action_auth.get(self._sub_action, self.auth_classes)
        if not auth_classes:
            auth_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
        return auth_classes

    @authentication_classes.setter
    def authentication_classes(self, value):
        self.auth_classes = value

    @property
    def _sub_action(self):
        return self._action_glossary.get(self._action)

    def get_serializer_class(self):
        assert isinstance(self.action_serializers, dict)
        serializer = self.action_serializers.get(self._action)
        if not serializer:
            return self.action_serializers.get(self._sub_action, super().get_serializer_class())
        return serializer

    def get_permissions(self):
        assert isinstance(self.action_permissions, dict)
        permission_classes = self.action_permissions.get(self._action)
        if not permission_classes:
            permission_classes = self.action_permissions.get(self._sub_action, self.permission_classes)
        if not permission_classes:
            permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
        return [permission() for permission in permission_classes]

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.action_queryset, dict)
        queryset = self.action_queryset.get(self._action)
        if queryset:
            setattr(self, "queryset", queryset)
        return super().get_queryset()

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_throttles(self):
        assert isinstance(self.action_throttle, dict)
        throttle_classes = self.action_throttle.get(self._action)
        if not throttle_classes:
            throttle_classes = self.action_throttle.get(self._sub_action, self.throttle_classes)
        return [throttle() for throttle in throttle_classes]
