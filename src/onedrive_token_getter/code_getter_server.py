from .common import OAUTH_REDIRECT_URI
from fastapi import FastAPI, Query, Response, status
from fastapi.responses import RedirectResponse
import dotenv
import os
from urllib.parse import quote
from .client import get_access_refresh_token

dotenv.load_dotenv()

server = FastAPI()
CODE = os.getenv("ONEDRIVE_AUTHENTICATION_CODE")
ACCESS_TOKEN = os.getenv("ONEDRIVE_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("ONEDRIVE_REFRESH_TOKEN")


@server.get("/login")
async def login():
    redirect_uri = quote(OAUTH_REDIRECT_URI)
    scope = quote("offline_access files.readwrite.all")
    return RedirectResponse(
        url = f"""https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
client_id={os.getenv("MICROSOFT_APP_CLIENT_ID")}
&response_type=code
&redirect_uri={redirect_uri}
&response_model=query
&scope={scope}"""
    )

@server.get("/oauth2/callback", status_code=200)
async def set_code(code: str):
    CODE = code
    return {"code":code}

@server.get("/code")
async def get_code():
    if not CODE:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return {"code" : CODE}

@server.get("/tokens")
async def get_tokens():
    if ACCESS_TOKEN is None and REFRESH_TOKEN is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return {"access_token" : ACCESS_TOKEN if ACCESS_TOKEN else None,
            "refresh_token" : REFRESH_TOKEN if REFRESH_TOKEN else None}

@server.get("/tokens/access_token")
async def get_access_token():
    if ACCESS_TOKEN is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    return {"access_token" : ACCESS_TOKEN}

@server.get("tokens/refresh_token")
async def get_refresh_token():
    if REFRESH_TOKEN is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    
    return {"refresh_token" : REFRESH_TOKEN}

