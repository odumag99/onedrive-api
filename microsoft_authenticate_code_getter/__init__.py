import uvicorn
import uvicorn.server
import asyncio
import threading
import time

# 멀티스레드 공유 객체 생성
# 멀티스레드에서 구동되는 server와 값을 공유받을 수 있도록 함.
__shared_val = {} # 딕셔너리는 Thread-safe(스레드간 공유되는) 객체

# 이벤트 생성
# server에서 호출하면 get_code() 함수가 재개될 수 있도록 Event 생성
__is_code_setted = threading.Event()

__config = uvicorn.Config(
    app = "microsoft_authenticate_code_getter.code_getter_server_app:app", # uvicorn app 정보
    port = 8000,
    reload=True,
    ssl_certfile="./openssl-certs/cert.pem", 
    ssl_keyfile="./openssl-certs/key.pem"
)
__server = uvicorn.Server(__config)

def __run_server():
    '''
    FastAPI 서버를 생성 및 실행하기 위한 Thread target 함수.
    '''
    asyncio.run(__server.serve())
    

def get_code():
    '''
    Microsoft로부터 Authentication code를 받기 위한 서버를 생성하고 code를 반환받는 함수.
    '''
    #TODO 서버 정상 종료를 위한 KeyboardInterrupt 예외 처리

    # code_getter_server 생성 및 실행
    # 별도 서버를 생성하기 위한 스레드
    print("서버를 생성하고 구동합니다.")
    code_getter_server_thread = threading.Thread(target=__run_server, daemon=True)
    code_getter_server_thread.start()

    #TODO 로그인 창 실행

    # get_code 완료 확인 때까지 wait
    print("code 반환 대기중입니다.")
    __is_code_setted.wait()

    # code 반환 완료 후 안내
    print(f"code가 반환되었습니다. code: {__shared_val["code"]}")

    # 서버 종료
    __server.should_exit = True
    print("서버를 종료를 위해 서버 종료 시그널을 보냈습니다.")
    
    # 종료를 위한 time.sleep()
    time.sleep(5)

    return __shared_val["code"]