def generate_code(story) -> str:
    summary = story.summary or "No summary"
    description = story.description or "No description"

    code = f"# Generated code based on story: {summary}\n"
    code += f"# Description: {description}\n\n"
    code += "def generated_function():\n"
    code += "    pass  # TODO: Implement"

    return code
