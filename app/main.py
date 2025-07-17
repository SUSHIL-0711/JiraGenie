from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print(payload)  # log the story data
    return {"received": True}
