import json

from fastapi import Request
from authx import exceptions

from .exceptions import MissingAccessJWTTokenError, AccessJWTDecodeError
from .jwt_security import security


async def TokenValidatorUseCase(request: Request) -> list:
    """
    Выполняет процесс проверки наличия и валидности jwt токена доступа.

    :param request: Информация пользователя.

    :return: Информация сохранённая в jwt токене: набор файлов необходимый к отправке.
    """

    try:
        access_payload = await security.access_token_required(request)
    except exceptions.MissingTokenError as e:
        raise MissingAccessJWTTokenError(f"Undefined token in cookie")
    except exceptions.JWTDecodeError as e:
        raise AccessJWTDecodeError(f"Invalid token or the access token has expired.")

    data = json.loads(access_payload.sub)
    return data

