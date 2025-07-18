from fastapi import FastAPI, Request
from app.jira_handler import parse_and_generate_code

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/webhook")
async def jira_webhook(request: Request):
    payload = await request.json()

    # Parse and generate code in one step
    story, generated_code = parse_and_generate_code(payload)

    print(f"📌 Parsed Story: {story}")
    print(f"🧾 Generated Code:\n{generated_code}")

    return {
        "received": True,
        "story": story,
        "generated_code": generated_code,
    }
