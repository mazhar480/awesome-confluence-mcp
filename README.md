# 🚀 Awesome Confluence MCP Server

**The most token-efficient way for AI agents to browse and analyze Confluence documentation.**

[![MCP](https://img.shields.io/badge/MCP-Compatible-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

<a href="https://glama.ai/mcp/servers/@mazhar480/awesome-confluence-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@mazhar480/awesome-confluence-mcp/badge" alt="Glama MCP Server Badge" />
</a>

**Topics:** `mcp-server` `python` `confluence-api` `ai-agents` `token-optimization` `markdown` `fastmcp`

---

## 📊 Token Savings at a Glance

**Typical Confluence Page (2,000 words):**

| Format | Tokens (Avg) | Cost (GPT-4o) | Savings |
|--------|--------------|---------------|---------|
| Raw HTML | 2,500 | $0.075 | - |
| **Your Markdown** | **600** | **$0.018** | **76%** |

> **Save 60-80% on LLM tokens** by converting Confluence pages to clean Markdown format.

A professional Model Context Protocol (MCP) server that provides token-efficient Confluence integration. Fetch, search, and convert Confluence pages to Markdown, dramatically reducing token consumption while preserving formatting and structure.

## 💡 Why Markdown Matters

**The Token-Saving Advantage:**

When working with LLMs, every token counts. Confluence pages in raw HTML format consume **3-5x more tokens** than the same content in Markdown:

- **HTML Format:** ~2,500 tokens for a typical page
- **Markdown Format:** ~500-800 tokens for the same page
- **Savings:** 60-80% reduction in token usage

This means:
- ✅ **Lower API costs** - Fewer tokens = less money spent
- ✅ **Faster responses** - Less data to process
- ✅ **Better context** - Fit more pages in your context window
- ✅ **Cleaner output** - Markdown is easier for LLMs to understand and work with

## ✨ Features

- **🔍 List Spaces** - Browse all accessible Confluence spaces
- **🔎 Search Pages** - Find pages by title or content with optional space filtering
- **📄 Fetch as Markdown** - Convert any Confluence page to clean, token-efficient Markdown
- **🔐 Secure Authentication** - Uses Atlassian API tokens (never store passwords)
- **⚡ Fast & Reliable** - Built with FastMCP for optimal performance
- **🛡️ Error Handling** - Comprehensive validation and helpful error messages

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/mazhar480/awesome-confluence-mcp.git
cd awesome-confluence-mcp

# Install with pip
pip install -e .
```

### 2. Get Your Atlassian API Token

1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Give it a name (e.g., "MCP Server")
4. Copy the token (you won't see it again!)

### 3. Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_EMAIL=your.email@example.com
CONFLUENCE_API_TOKEN=your_api_token_here
```

### 4. Configure Your MCP Client

#### For Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "confluence": {
      "command": "python",
      "args": ["-m", "server"],
      "cwd": "/path/to/awesome-confluence-mcp",
      "env": {
        "CONFLUENCE_URL": "https://your-domain.atlassian.net",
        "CONFLUENCE_EMAIL": "your.email@example.com",
        "CONFLUENCE_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

#### For Cline (VS Code Extension)

Add to your MCP settings:

```json
{
  "confluence": {
    "command": "python",
    "args": ["-m", "server"],
    "cwd": "/path/to/awesome-confluence-mcp"
  }
}
```

Make sure your `.env` file is configured in the project directory.

## 🔧 Available Tools

### `list_spaces`

List all Confluence spaces you have access to.

**Parameters:**
- `limit` (optional): Maximum number of spaces to return (1-100, default: 25)

**Example:**
```
List my Confluence spaces
```

**Returns:**
```json
{
  "total": 3,
  "spaces": [
    {
      "key": "DOCS",
      "name": "Documentation",
      "type": "global",
      "id": "123456",
      "url": "https://your-domain.atlassian.net/wiki/spaces/DOCS"
    }
  ]
}
```

### `search_pages`

Search for pages by title or content.

**Parameters:**
- `query` (required): Search term to match against titles and content
- `space_key` (optional): Limit search to a specific space
- `limit` (optional): Maximum results to return (1-50, default: 10)

**Example:**
```
Search for pages about "API documentation" in the DOCS space
```

**Returns:**
```json
{
  "total": 5,
  "query": "API documentation",
  "space_key": "DOCS",
  "pages": [
    {
      "id": "789012",
      "title": "REST API Documentation",
      "type": "page",
      "space": {
        "key": "DOCS",
        "name": "Documentation"
      },
      "version": 12,
      "url": "https://your-domain.atlassian.net/wiki/spaces/DOCS/pages/789012"
    }
  ]
}
```

### `fetch_page_markdown`

Fetch a page and convert it to Markdown format.

**Parameters:**
- `page_id` (required): The Confluence page ID

**Example:**
```
Fetch page 789012 as markdown
```

**Returns:**
```markdown
# REST API Documentation

**Space:** Documentation (DOCS)
**Version:** 12
**URL:** https://your-domain.atlassian.net/wiki/spaces/DOCS/pages/789012
**Labels:** api, rest, documentation

---

## Overview

This page documents our REST API endpoints...

### Authentication

All requests require an API token...
```

## 🎯 Usage Examples

### Example 1: Find and Read Documentation

```
1. "List my Confluence spaces"
2. "Search for 'onboarding' pages in the HR space"
3. "Fetch page 123456 as markdown"
```

### Example 2: Research a Topic

```
"Search for pages about 'authentication' and fetch the top 3 results as markdown"
```

The MCP server will:
1. Search for relevant pages
2. Return the search results
3. Fetch each page and convert to Markdown
4. Provide clean, token-efficient content for analysis

## 🔒 Security Best Practices

- ✅ **Never commit** your `.env` file to version control
- ✅ **Use API tokens** instead of passwords
- ✅ **Rotate tokens** regularly
- ✅ **Limit token scope** to only what's needed
- ✅ **Store tokens securely** in environment variables

## 🛠️ Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Lint code
ruff check .
```

## 🧪 Testing with MCP Inspector

Want to test the tools without writing a full client? FastMCP includes a built-in MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python server.py
```

This launches a web interface where you can:
- ✅ Test all three tools interactively
- ✅ See real-time request/response data
- ✅ Validate your Confluence credentials
- ✅ Experiment with different parameters

**Perfect for:** Quick testing, debugging, and demonstrating the server to others.

## 💰 Sponsorship & Support

If this MCP server saves you time and tokens, consider sponsoring its development:

- **Individual Developers:** [GitHub Sponsors](https://github.com/sponsors/mazhar480)
- **Corporate Teams:** I support **GitHub Invoiced Billing** for bulk sponsorships. [Contact me](mailto:your.email@example.com) for custom MCP development and enterprise support.

**Why sponsor?**
- Priority bug fixes and feature requests
- Custom tool development for your workflow
- Direct support and consultation
- Help maintain this free, open-source tool

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Atlassian Confluence API](https://developer.atlassian.com/cloud/confluence/rest/v2/)
- Markdown conversion by [markdownify](https://github.com/matthewwithanm/python-markdownify)

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/mazhar480/awesome-confluence-mcp/issues)
- **Discussions:** [GitHub Discussions](https://github.com/mazhar480/awesome-confluence-mcp/discussions)

---

**Made with ❤️ for the MCP community**
