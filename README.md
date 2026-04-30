# mcp-github-server

A Python-based [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that connects **Claude Desktop** directly to GitHub — letting you manage repositories, push code, open issues, and more, all through natural language.



---

## Features

| Tool | Description |
|------|-------------|
| `create_repo` | Create a new public or private GitHub repository |
| `push_file` | Push or update a file in any repository |
| `create_issue` | Open a new issue with a title and description |
| `list_repos` | List all repositories for the authenticated user |
| `generate_readme` | Use an AI subagent to auto-generate a README for a repo |
| `summarize_repo` | Use an AI subagent to summarize a repo's purpose and contents |

---

## How It Works

This server implements the MCP protocol, exposing GitHub actions as tools that Claude Desktop can call during a conversation. When you ask Claude to "create a repo" or "push this file to GitHub", it routes the request through this server using the GitHub API.

AI-powered tools like `generate_readme` and `summarize_repo` spin up subagents that analyze repository content and produce human-readable output — no manual prompting required.

---

## Getting Started

### Prerequisites

- Python 3.9+
- A GitHub [Personal Access Token](https://github.com/settings/tokens) with `repo` scope
- [Claude Desktop](https://claude.ai/download) with MCP support

### Installation

```bash
git clone https://github.com/Ajay43634/mcp-github-server.git
cd mcp-github-server
pip install -r requirements.txt
```

### Configuration

Set your GitHub token as an environment variable:

```bash
export GITHUB_TOKEN=your_personal_access_token
```

### Connecting to Claude Desktop

Add the following to your Claude Desktop MCP config file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "github": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "GITHUB_TOKEN": "your_personal_access_token"
      }
    }
  }
}
```

Then restart Claude Desktop — the GitHub tools will be available automatically.

---

## Example Usage

Once connected, you can use natural language in Claude Desktop:

- *"Create a new public repo called my-project"*
- *"Push my main.py file to my-project"*
- *"Open an issue in my-project titled 'Fix authentication bug'"*
- *"List all my GitHub repositories"*
- *"Generate a README for my-project"*
- *"Summarize what my-project does"*

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgements

Built with the [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic and the [GitHub REST API](https://docs.github.com/en/rest).
