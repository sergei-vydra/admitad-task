ACCOUNT_EMAIL_REQUIRED: bool = True
ACCOUNT_UNIQUE_EMAIL: bool = True
ACCOUNT_EMAIL_VERIFICATION: str = "mandatory"

REST_AUTH: dict[str, str | bool] = {
    "LOGIN_SERIALIZER": "app.users.serializers.users.LoginSerializer",
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
    "OLD_PASSWORD_FIELD_ENABLED": True,
}
