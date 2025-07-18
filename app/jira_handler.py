from pydantic import BaseModel
from app.generator import generate_code

class JiraStory(BaseModel):
    key: str
    summary: str
    description: str | None = None

def parse_story(payload: dict) -> JiraStory:
    fields = payload.get("issue", {}).get("fields", {})
    story = JiraStory(
        key=payload.get("issue", {}).get("key", ""),
        summary=fields.get("summary", ""),
        description=fields.get("description", ""),
    )
    return story

def parse_and_generate_code(payload: dict) -> tuple[JiraStory, str]:
    """
    Parses the payload and immediately generates code from the parsed story.
    """
    story = parse_story(payload)
    code = generate_code(story)
    return story.dict(), code
