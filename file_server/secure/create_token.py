import structlog
import json

from .jwt_security import security
from file_server.config import Settings

logger = structlog.get_logger(__name__)

settings: Settings = Settings()

async def CreateToken(data: list[str] | str) -> dict[str, bool|str]:
    """
    Выполняет процесс создания jwt токенов доступа.

    :param data: Информация, для сохранения в jwt.
    :param response: Доступ к ответу пользователю.

    :return: Словарь с результатом выполнения, access token и refresh token.
    """
    if type(data) is not str:
        data = json.dumps(data)
    access_token = security.create_access_token(data)

    logger.debug(
        "Create tokens completed",
        data=data
    )

    return {"ok": True, "access_token": access_token}
