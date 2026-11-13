from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from file_server.logging_setup import setup_logging
from file_server.secure.jwt_security import security
from file_server.routers import api_v1_router
from file_server.error_handling import setup_exception_handlers


setup_logging()
logger = structlog.get_logger(__name__)



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """

    :param _:
    :return:
    """
    logger.info("Starting application")
    yield
    logger.info("Shutting down application")

def create_app() -> FastAPI:
    """

    :return:
    """

    app = FastAPI(
        title="WS",
        version="1.0.0",
        description="WS",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    setup_exception_handlers(app)
    app.include_router(api_v1_router, prefix="/api")
    security.handle_errors(app)

    return app


app = create_app()
#
# if __name__ == '__main__':
#     uvicorn.run("file_server:app", host="127.0.0.1", port=10001, reload=True)