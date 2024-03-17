from api import settings

USE_BROWSABLE_API: bool = settings.env("USE_BROWSABLE_API")

SPECTACULAR_SETTINGS = {
    "TITLE": f"{settings.env('SITE_NAME')} API",
    "DISABLE_ERRORS_AND_WARNINGS": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {"docExpansion": "none"},
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.11.5",
}
