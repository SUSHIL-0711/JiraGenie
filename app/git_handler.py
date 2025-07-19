import subprocess
import os

REPO_PATH = os.getcwd()

def run_git_command(command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=REPO_PATH,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Git command failed: {' '.join(command)}\n{result.stderr}")
    return result.stdout.strip()


def create_branch(branch_name: str):
    result = subprocess.run(
        ["git", "branch", "--list", branch_name],
        cwd=REPO_PATH,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.stdout.strip():
        print(f"✅ Branch {branch_name} already exists, checking it out.")
        run_git_command(["git", "checkout", branch_name])
    else:
        print(f"🌱 Creating new branch {branch_name}.")
        run_git_command(["git", "checkout", "-b", branch_name])


def commit_all_changes(commit_message: str) -> None:
    run_git_command(["git", "add", "."])
    run_git_command(["git", "commit", "-m", commit_message])


def push_branch(branch_name: str) -> None:
    run_git_command(["git", "push", "-u", "origin", branch_name, "--force"])


def create_pull_request(branch_name: str, title: str, body: str) -> str:
    result = subprocess.run(
        ["gh", "pr", "create", "--head", branch_name, "--title", title, "--body", body],
        cwd=REPO_PATH,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Failed to create PR: {result.stderr}")
    return result.stdout.strip()
