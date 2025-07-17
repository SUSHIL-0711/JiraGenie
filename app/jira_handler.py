def parse_jira_payload(payload: dict) -> dict:
    """
    Parse incoming Jira webhook payload and extract story details.
    """
    issue = payload.get("issue", {})
    fields = issue.get("fields", {})

    story = {
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "issuetype": fields.get("issuetype", {}).get("name"),
        "status": fields.get("status", {}).get("name"),
        "reporter": fields.get("reporter", {}).get("displayName"),
    }
    return story
