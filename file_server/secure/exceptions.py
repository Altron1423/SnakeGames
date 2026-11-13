from typing import final

@final
class MissingAccessJWTTokenError(Exception):
    """Исключение возникает при отсутствии JWT токена."""

@final
class AccessJWTDecodeError(Exception):
    """Исключение возникает при некорректном JWT или истечении его времени действия."""
