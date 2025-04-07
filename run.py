import src.onedrive_api as fastapi
import uvicorn

app = fastapi.app

if __name__ == "__main__":
    uvicorn.run(app="src.onedrive_api:app",
                port=8000,
                reload=True, 
                ssl_certfile="./openssl-certs/cert.pem", 
                ssl_keyfile="./openssl-certs/key.pem"
    )