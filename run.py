import uvicorn


if __name__ == "__main__":
    uvicorn.run(app="src.onedrive_token_getter:app",
                port=8000,
                reload=True, 
                ssl_certfile="./openssl-certs/cert.pem", 
                ssl_keyfile="./openssl-certs/key.pem"
    )