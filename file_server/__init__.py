# import uvicorn

# import main
# print(main.__file__)
# print([n for n in dir(main) if not n.startswith('_')])
from .main import app
# if __name__ == '__main__':
#     uvicorn.run("file_server:app", host="127.0.0.1", port=10001, reload=True)
#     ...