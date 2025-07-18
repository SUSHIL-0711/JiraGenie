from fastapi import FastAPI, Request
from app.jira_handler import parse_jira_payload
from app.generator import generate_code

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/webhook")
async def jira_webhook(request: Request):
    payload = await request.json()
    story = parse_jira_payload(payload)

    print(f"📌 Parsed Story: {story}")

    # Call the code generator
    generated_code = generate_code(story)

    print(f"🧾 Generated Code:\n{generated_code}")

    return {
        "received": True,
        "story": story,
        "generated_code": generated_code,
    }
