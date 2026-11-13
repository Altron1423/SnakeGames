from pathlib import Path
from requests import Response


def save_file(target_dir: Path, request: Response):
    target_path = target_dir / request.headers["X-File-Path"]
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w") as f:
        f.write(request.text)
