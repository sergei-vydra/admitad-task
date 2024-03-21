from rest_framework import filters

__all__ = ["IsOwnerFilterBackend", "IsBelongReminderFilterBackend"]


class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class IsBelongReminderFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return (queryset.filter(user=request.user) | queryset.filter(recipients__in=[request.user])).distinct()
