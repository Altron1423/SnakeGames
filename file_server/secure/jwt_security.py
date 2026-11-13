import hashlib
from datetime import timedelta

from authx import AuthX, AuthXConfig

from file_server.config import Settings

def create_security(
        settings: Settings,
)->AuthX:
    config = AuthXConfig()

    config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    config.JWT_SECRET_KEY = settings.jwt_secret_key
    config.JWT_ACCESS_COOKIE_NAME = settings.jwt_access_cookie_name
    config.JWT_COOKIE_CSRF_PROTECT = settings.jwt_cookie_csrf_protect
    config.JWT_TOKEN_LOCATION = settings.jwt_token_location
    config.JWT_ALGORITHM = settings.jwt_algorithm

    security = AuthX(config=config)
    return security

security = create_security(Settings())

hash_model = hashlib.sha1
