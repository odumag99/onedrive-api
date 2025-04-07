import uvicorn
import uvicorn.server
import asyncio
import threading
import time

from .code_getter_server import CODE
from .client import get_code, get_access_refresh_token

config = uvicorn.Config(
    app = "code_getter_server:server",
    port = 8000,
    reload=True,
    ssl_certfile="./openssl-certs/cert.pem", 
    ssl_keyfile="./openssl-certs/key.pem"
)
server = uvicorn.Server(config)

def run_server():
    print("서버를 생성합니다.")
    asyncio.run(server.serve())
    print("서버 생성이 완료되었습니다.")
    

def get_code():
    # code_getter_server 자동 생성
    code_getter_server_thread = threading.Thread(target=run_server, daemon=True)
    code_getter_server_thread.start()

    # 로그인 창 실행

    # get_code 완료 확인 때까지 wait
    print("code 반환 대기중입니다.")
    while CODE is None:
        pass
    print(f"code가 반환되었습니다. code: {CODE}")

    # 서버 종료
    print("서버를 종료합니다.")
    server.should_exit = True
    print("서버 종료 시그널을 보냈습니다.")

    time.sleep(5)
    

    # code 얻어 access_token, refresh_token
    # code = get_code()

    # refresh_token, access_token = get_access_refresh_token()
    # print({
    #     "refresh_token" : refresh_token,
    #     "access_token" : access_token
    # })