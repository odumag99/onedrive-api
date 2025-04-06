import httpx
import dotenv
import os
from .common import OAUTH_REDIRECT_URI

dotenv.load_dotenv()

async def get_token(code: str):
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

    
    return res.json()