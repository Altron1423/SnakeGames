import uvicorn

if __name__ == '__main__':
    uvicorn.run("file_server:app", host="192.168.1.241", port=10001)
