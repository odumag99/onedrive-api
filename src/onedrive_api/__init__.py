from fastapi import FastAPI

app = FastAPI()

@app.get("/callback")
async def callback()