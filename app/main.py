from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
from app.jira_handler import parse_jira_payload

load_dotenv()
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    story = parse_jira_payload(payload)
    print("📌 Parsed Story:", story)
    return {"received": True, "story": story}
