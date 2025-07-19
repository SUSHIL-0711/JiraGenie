from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
from app.jira_handler import parse_and_generate_code
from app.git_handler import (
    create_branch,
    commit_all_changes,
    push_branch,
    create_pull_request,
)
import os

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}


def save_generated_code(story_key: str, generated_code: str) -> str:
    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{story_key.replace('-', '_').lower()}.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(generated_code)
    print(f"💾 Generated code saved to: {filename}")
    return filename


@app.post("/webhook")
async def jira_webhook(request: Request):
    payload = await request.json()

    story, generated_code = parse_and_generate_code(payload)

    print(f"📌 Parsed Story: {story}")
    print(f"🧾 Generated Code:\n{generated_code}")

    branch_name = f"{story['key']}-{story['summary'].replace(' ', '-').lower()}"
    commit_message = f"Code for {story['key']} - {story['summary']}"
    pr_title = f"PR for {story['key']} - {story['summary']}"
    pr_body = story.get("description") or "Auto-generated PR from JiraGenie"

    try:
        # Save file first
        file_path = save_generated_code(story["key"], generated_code)

        create_branch(branch_name)
        print(f"🌿 Created branch: {branch_name}")

        commit_all_changes(commit_message)
        push_branch(branch_name)
        print(f"✅ Committed and pushed changes to remote")

        pr_url = create_pull_request(branch_name, pr_title, pr_body)
        print(f"🔗 PR created: {pr_url}")

    except Exception as e:
        print(f"🚨 Error during Git/PR flow: {e}")
        return {
            "received": True,
            "story": story,
            "generated_code": generated_code,
            "error": str(e),
        }

    return {
        "received": True,
        "story": story,
        "generated_code": generated_code,
        "branch": branch_name,
        "pr_url": pr_url,
    }
