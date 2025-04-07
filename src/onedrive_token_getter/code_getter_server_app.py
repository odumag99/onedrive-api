from .common import OAUTH_REDIRECT_URI
from fastapi import FastAPI, Response, status, BackgroundTasks
from fastapi.responses import RedirectResponse
import dotenv
import os
from urllib.parse import quote

from . import shared_val, is_code_setted

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

def is_code_setted_set():
    is_code_setted.set()

@app.get("/oauth2/callback", status_code=200)
async def set_code(code: str, backgroundtasks: BackgroundTasks):
    shared_val["code"] = code
    backgroundtasks.add_task(is_code_setted_set)
    return { "code" : shared_val["code"] }

@app.get("/code")
async def get_code():
    if not shared_val["code"]:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return { "code" : shared_val["code"] }


