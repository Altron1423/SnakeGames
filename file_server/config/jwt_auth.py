from pathlib import Path
from typing import final, Literal
from collections.abc import Sequence

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings


@final
class JWTSettings(BaseSettings):
    """
    Параметры конфигурации базы данных.

    Attributes:
        jwt_secret_key (str): ключ шифровки для jwt.
        jwt_access_cookie_name (str): Название активного jwt токена в cookie.
        jwt_cookie_csrf_protect (bool): Защита от межсайтовой подделки запросов.
        jwt_token_location (Sequence[Literal["headers", "cookies", "json", "query"]]):
            Места, из которых будет приниматься jwt токен.
        jwt_algorithm (Literal[
        "HS256", "HS384", "HS512", "ES256", "ES256K",
        "ES384", "ES512", "RS256", "RS384", "RS512",
        "PS256", "PS384", "PS512"]):
            алгоритм кодировки.
    """

    jwt_secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    jwt_access_cookie_name: str = Field(..., alias="JWT_ACCESS_COOKIE_NAME")
    jwt_cookie_csrf_protect: bool = Field(..., alias="JWT_COOKIE_CSRF_PROTECT")
    jwt_token_location: Sequence[Literal[
        "headers", "cookies", "json", "query"
    ]] = Field(..., alias="JWT_TOKEN_LOCATION")
    jwt_algorithm: Literal[
        "HS256",
        "HS384",
        "HS512",
        "ES256",
        "ES256K",
        "ES384",
        "ES512",
        "RS256",
        "RS384",
        "RS512",
        "PS256",
        "PS384",
        "PS512"
    ] = Field(..., alias="JWT_ALGORITHM")
    hash_algorithm: Literal[
        'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
        'blake2b', 'blake2s',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
        'shake_128', 'shake_256'
    ] = Field(..., alias="HASH_ALGORITHM")



    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
