import asyncio
from pathlib import Path

import requests

from file_server.secure.create_token import CreateToken



token:str = asyncio.run(
    CreateToken(
        ["map/block/start_test.json", "map/chunk/test_chunk.json"]
    )
)["access_token"]

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJbXCJlbnRpdGllcy96b21iaWUuanNvblwiXSIsImp0aSI6IjljOWM2YmNiLWUwMTAtNGRmYS05ZTIzLWM0ZWE1ZDM5NjhmNyIsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2UsImNzcmYiOiIiLCJpYXQiOjE3OTQ1ODQ3MTksImV4cCI6MTc5NTQ0ODcxOS4wOTk4OTF9.sbdgNFD66QfqMQFYgeKWPai-Hq-be2gjZHFa3RWOwWg'
cookies={"access_token": token}

target_dir = Path("/home/altron/PycharmProjects/SnakeGames/dop_assets")

def download(file_id: int):
    url = f"http://192.168.1.241:10001/api/download_files/{file_id}"

    user_agent = {"User-Agent": "Mozilla/5.0"}

    request = requests.get(url, headers=user_agent, cookies=cookies)
    return request

def save_file(target_dir: Path, request: requests.Response):
    target_path = target_dir / request.headers["X-File-Path"]
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w") as f:
        f.write(request.text)

if __name__ == "__main__":
    for i in range(2):
        req = download(i)
        print(f"{i}:")
        print(f"\t{req.status_code}")
        print(f"\t{req.text}")
        save_file(target_dir, req)
        # print(f"\t{req.headers}")
