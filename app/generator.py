def generate_code(story: dict) -> str:
    """
    Generate starter code based on the Jira story details.
    For now, this is a mock implementation.
    """
    summary = story.get("summary", "No summary")
    description = story.get("description", "")

    # TODO: Replace this with real StarCoder integration
    generated_code = f"""\
# Task: {summary}
# Description: {description}

def main():
    print("Hello from generated code for: {summary}")
"""

    return generated_code
