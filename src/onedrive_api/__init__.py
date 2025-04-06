from .common import OAUTH_REDIRECT_URI
from fastapi import FastAPI, Query, Response
from fastapi.responses import RedirectResponse
import dotenv
import os
from urllib.parse import quote
from .token_getter import get_token

dotenv.load_dotenv()

app = FastAPI()


@app.get("/login")
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

@app.get("/oauth2/callback", status_code=200)
async def get_code(code: str):
    get_token(code)
    return Response(status_code=200)