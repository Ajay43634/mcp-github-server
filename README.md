# mcp-github-server

A GitHub integration built on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), enabling AI assistants like Claude to interact with GitHub repositories directly.

## Features

- 📁 **Create Repositories** — Spin up new public or private GitHub repos
- 📄 **Push Files** — Create or update files with custom commit messages
- 🐛 **Create Issues** — Open issues with titles and descriptions
- 📋 **List Repositories** — View all repos for the authenticated user
- 🔍 **Summarize Repos** — Get an AI-generated summary of any repository

## Getting Started

### Prerequisites

- Python 3.9+
- A GitHub Personal Access Token with `repo` scope
- An MCP-compatible host (e.g. Claude Desktop, Claude.ai)

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

## Usage

Once connected to an MCP host, you can use natural language commands like:

- *"Create a new public repo called my-project"*
- *"Push a README to my-project"*
- *"List all my repositories"*
- *"Open an issue in my-project titled 'Fix login bug'"*

## MCP Tool Reference

| Tool | Description |
|------|-------------|
| `create_repo` | Create a new GitHub repository |
| `push_file` | Push a file to a repository |
| `create_issue` | Open a new issue |
| `list_repos` | List all user repositories |
| `summarize_repo` | AI-powered repo summary |

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgements

Built with the [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic.
