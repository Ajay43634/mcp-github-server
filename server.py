"""
GitHub Automation MCP Server
=============================
Tools:
  - create_repo        → Create a new GitHub repository
  - push_file          → Push a file to a repository
  - create_issue       → Create an issue in a repository
  - list_repos         → List your GitHub repositories
  - generate_readme    → AI subagent generates + pushes a README
  - summarize_repo     → AI subagent summarizes a repo's contents

Subagents are used in generate_readme and summarize_repo —
they make a separate Claude API call so the main conversation
stays clean.
"""

import os
import base64
import anthropic

from dotenv import load_dotenv
from github import Github, GithubException
from mcp.server.fastmcp import FastMCP

# ── Load environment variables from .env ─────────────────────────────────────
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# ── Clients ───────────────────────────────────────────────────────────────────
gh = Github(GITHUB_TOKEN)
ai = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
mcp = FastMCP("github-server")


# ── HELPER: Subagent ──────────────────────────────────────────────────────────
def run_subagent(system_prompt: str, user_message: str) -> str:
    """
    Spins up a separate Claude API call (subagent).
    Only the final text result is returned — the subagent's
    full conversation is discarded, keeping the main context clean.
    """
    response = ai.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


# ── TOOLS ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def create_repo(name: str, description: str = "", private: bool = False) -> str:
    """
    Create a new GitHub repository.

    Args:
        name:        Repository name (e.g. 'my-project')
        description: Short description of the repo
        private:     Set True to make the repo private (default: public)

    Returns:
        The URL of the newly created repository.
    """
    try:
        user = gh.get_user()
        repo = user.create_repo(
            name=name,
            description=description,
            private=private,
            auto_init=False,
        )
        return f"Repo created: {repo.html_url}"
    except GithubException as e:
        return f"Error creating repo: {e.data.get('message', str(e))}"


@mcp.tool()
def push_file(repo_name: str, file_path: str, content: str, commit_message: str = "Add file") -> str:
    """
    Push (create or update) a file in a GitHub repository.

    Args:
        repo_name:      Repo name, e.g. 'ajayrao/my-project'
        file_path:      Path inside the repo, e.g. 'src/main.py'
        content:        The text content of the file
        commit_message: Git commit message

    Returns:
        Confirmation with the commit URL.
    """
    try:
        user = gh.get_user()
        full_name = f"{user.login}/{repo_name}" if "/" not in repo_name else repo_name
        repo = gh.get_repo(full_name)

        try:
            # File exists — update it
            existing = repo.get_contents(file_path)
            result = repo.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=existing.sha,
            )
        except GithubException:
            # File doesn't exist — create it
            result = repo.create_file(
                path=file_path,
                message=commit_message,
                content=content,
            )

        return f"File pushed: {result['commit'].html_url}"
    except GithubException as e:
        return f"Error pushing file: {e.data.get('message', str(e))}"


@mcp.tool()
def create_issue(repo_name: str, title: str, body: str = "") -> str:
    """
    Create a new issue in a GitHub repository.

    Args:
        repo_name: Repo name, e.g. 'my-project' or 'ajayrao/my-project'
        title:     Issue title
        body:      Issue description (optional)

    Returns:
        URL of the created issue.
    """
    try:
        user = gh.get_user()
        full_name = f"{user.login}/{repo_name}" if "/" not in repo_name else repo_name
        repo = gh.get_repo(full_name)
        issue = repo.create_issue(title=title, body=body)
        return f"Issue created: {issue.html_url}"
    except GithubException as e:
        return f"Error creating issue: {e.data.get('message', str(e))}"


@mcp.tool()
def list_repos() -> list[str]:
    """
    List all repositories for the authenticated GitHub user.

    Returns:
        List of repo names.
    """
    try:
        user = gh.get_user()
        return [repo.full_name for repo in user.get_repos()]
    except GithubException as e:
        return [f"Error: {e.data.get('message', str(e))}"]


@mcp.tool()
def generate_readme(repo_name: str, project_description: str) -> str:
    """
    Use an AI subagent to generate a professional README and push it to the repo.

    Args:
        repo_name:           Repo name, e.g. 'my-project'
        project_description: A short description of what the project does

    Returns:
        Confirmation that the README was pushed.
    """
    # Subagent generates the README content
    readme_content = run_subagent(
        system_prompt=(
            "You are a technical writer. Write a clean, professional GitHub README.md "
            "in Markdown format. Include: project title, description, features, "
            "installation steps, usage, and license sections. Be concise but thorough."
        ),
        user_message=f"Write a README for this project: {project_description}",
    )

    # Push the generated README to GitHub
    return push_file(
        repo_name=repo_name,
        file_path="README.md",
        content=readme_content,
        commit_message="Add AI-generated README",
    )


@mcp.tool()
def summarize_repo(repo_name: str) -> str:
    """
    Use an AI subagent to summarize the contents and purpose of a repository.

    Args:
        repo_name: Repo name, e.g. 'my-project' or 'ajayrao/my-project'

    Returns:
        A plain-English summary of the repository.
    """
    try:
        user = gh.get_user()
        full_name = f"{user.login}/{repo_name}" if "/" not in repo_name else repo_name
        repo = gh.get_repo(full_name)

        # Collect repo metadata and file list
        files = [f.path for f in repo.get_contents("")]
        info = (
            f"Repo: {repo.full_name}\n"
            f"Description: {repo.description}\n"
            f"Language: {repo.language}\n"
            f"Stars: {repo.stargazers_count}\n"
            f"Files: {', '.join(files)}"
        )

        # Subagent summarizes the repo
        return run_subagent(
            system_prompt=(
                "You are a code reviewer. Given repository metadata, write a clear "
                "2-3 sentence summary of what the project is and what it does."
            ),
            user_message=f"Summarize this GitHub repo:\n{info}",
        )
    except GithubException as e:
        return f"Error fetching repo: {e.data.get('message', str(e))}"


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")