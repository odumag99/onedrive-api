import uvicorn
import uvicorn.server
import asyncio
import threading
import time

from .client import get_code, get_access_refresh_token

# 멀티스레드 공유 객체 생성
shared_val = {} # 딕셔너리는 Thread-safe(스레드간 공유되는) 객체

# 이벤트 생성
is_code_setted = threading.Event()

config = uvicorn.Config(
    app = "src.onedrive_token_getter.code_getter_server:server",
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
    is_code_setted.wait()

    # code 반환 완료 후 안내내
    print(f"code가 반환되었습니다. code: {shared_val["code"]}")

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