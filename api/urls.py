from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = []

if settings.USE_BROWSABLE_API:
    urlpatterns += [
        path("__docs__/", SpectacularAPIView.as_view(), name="__docs__"),
        path("swagger", SpectacularSwaggerView.as_view(url_name="__docs__")),
    ]

urlpatterns += [
    path("api/v1/", include("app.urls")),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
)
