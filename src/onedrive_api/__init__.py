from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import dotenv
import os
from urllib.parse import quote

dotenv.load_dotenv()
app = FastAPI()

@app.get("/login")
async def login():
    scope = quote("offline_access files.readwrite.all")
    return RedirectResponse(
        url = f"""https://login.microsoftonline.com/common/oauth2/v2,0/authorize?
client_id={os.getenv("MICROSOFT_APP_CLIENT_ID")}
&response_type=code
&redirect_uri=http://{os.getenv("FRONT_URL")}/oauth2/callback
&response_model=query
&scope={scope}"""
    )