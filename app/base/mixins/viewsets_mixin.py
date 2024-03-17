from rest_framework.mixins import CreateModelMixin as BaseCreateModelMixin
from rest_framework.mixins import DestroyModelMixin as BaseDestroyModelMixin
from rest_framework.mixins import UpdateModelMixin as BaseUpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

__all__ = ["CreateModelMixin", "UpdateModelMixin", "DestroyModelMixin"]


class CreateModelMixin(BaseCreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = self.get_queryset().get(pk=serializer.instance.pk)

        if self.action_serializers.get("create_display"):
            serializer = self.action_serializers["create_display"](instance=instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class UpdateModelMixin(BaseUpdateModelMixin):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if self.action_serializers.get("update_display"):
            instance = self.get_object()
            serializer = self.action_serializers["update_display"](instance=instance)
        else:
            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}
        return Response(serializer.data)


class DestroyModelMixin(BaseDestroyModelMixin):
    soft_delete = False

    def perform_destroy(self, instance):
        if self.soft_delete or hasattr(instance, "is_deleted"):
            instance.update(**{"is_deleted": True})
        else:
            super().perform_destroy(instance)
