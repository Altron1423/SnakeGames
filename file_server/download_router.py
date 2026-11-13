from pathlib import Path


from fastapi import APIRouter, Request
from starlette.responses import FileResponse

from file_server.secure.token_validator import TokenValidatorUseCase

router = APIRouter(prefix="", tags=["Download"])


@router.get(
    "/download_files/{file_id}",
    summary="return 1",
)
async def download(
    request: Request,
    file_id: int
# ) -> dict[str, str | FileResponse]:
):
    """
    Тестовая команда, для проверки работы функции проверки валидности jwt токена.
    :param request:
    :return:
    """
    files_for_download = await TokenValidatorUseCase(request)
    target_file = files_for_download[file_id]

    directory = Path("/home/altron/PycharmProjects/SnakeGames/src/data")
    print(directory)
    file_path = directory / target_file

    if not file_path.is_file():
        raise FileNotFoundError
    return FileResponse(
        str(file_path),
        headers={
            "X-File-Path": str(target_file),  # ← метаданные в заголовке
            # "X-Content-SHA256": sha256_cached(path),
        },
        status_code=200
    )
    # return {
    #     "file_path": str(target_file),
    #     "file": FileResponse(str(file_path), status_code=200)
    # }
