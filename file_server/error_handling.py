from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from file_server.secure.exceptions import (
    MissingAccessJWTTokenError,
    AccessJWTDecodeError,
)

from .exceptions import FileNotFoundError


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Добавленные сюда исключения не будут срабатывать как ошибка и вылетать в консоль.
    Вместо этого они отправятся клиенту в описанном тут формате, можно настроить код и оформление исключения.
    exc - сообщение переданное в исключение при вызове в коде.

    :param app: Экземпляр приложения FastAPI, для которого необходимо добавить исключения
    :return:
    """


    @app.exception_handler(MissingAccessJWTTokenError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: MissingAccessJWTTokenError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(AccessJWTDecodeError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: AccessJWTDecodeError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": str(exc)},
        )

    @app.exception_handler(FileNotFoundError)
    async def email_been_used_exception_handler(
        request: Request,
        exc: FileNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )
