import httpx
import dotenv
import os
from typing import Tuple
from .common import OAUTH_REDIRECT_URI

dotenv.load_dotenv()
TOKEN_GETTER_SERVER_URI = f"https://{os.getenv("FRONT_URL")}"

async def get_access_refresh_token(code: str):
    url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    client_id = os.getenv("MICROSOFT_APP_CLIENT_ID")
    grant_type = "authorization_code"
    scope = "offline_access files.readwrite.all"
    code = code
    redirect_uri = OAUTH_REDIRECT_URI
    form = {"client_id":client_id,
            "grant_type":grant_type,
            "scope":scope,
            "code":code,
            "redirect_uri":redirect_uri,
            "client_secret":os.getenv("MICROSOFT_APP_CLIENT_SECRET")
            }
    async with httpx.AsyncClient() as client:
        res = await client.post("https://login.microsoftonline.com/common/oauth2/v2.0/token",
                        headers={"Content-Type":"application/x-www-form-urlencoded"},
                        data=form
        # )
        # res = await client.post("https://login.microsoftonline.com/common/oauth2/v2.0/token",
        #                         json=form
        )
    res.raise_for_status()

    res_json = res.json()
    if not res_json["access_token"] or not res_json["refresh_token"]:
        raise Exception(res)

    return res_json["access_token"], res_json["refresh_token"]

async def get_code() -> str: 
    async with httpx.AsyncClient() as client:
        res = await client.get(
            url = TOKEN_GETTER_SERVER_URI + f"/code"
        )

        res.raise_for_status()

        res_json = res.json()

        if not res_json["code"]:
            raise Exception(res)
        
        return res_json["code"]
