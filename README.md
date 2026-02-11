# ConfluenceLens MCP Server

A Model Context Protocol (MCP) server that fetches Confluence pages and converts them to clean Markdown format. Built with FastMCP.

## Features

- 🔍 Fetch Confluence pages by page ID
- 📝 Convert Confluence storage format (HTML) to clean Markdown
- 🔐 Secure authentication using Atlassian API tokens
- ⚡ Fast and lightweight using FastMCP framework

## Installation

### Prerequisites

- Python 3.8 or higher
- An Atlassian account with API access
- Confluence site access

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/confluencelens.git
cd confluencelens
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:

Create a `.env` file or set the following environment variables:

```bash
ATLASSIAN_USER_EMAIL=your.email@example.com
ATLASSIAN_API_TOKEN=your_api_token_here
CONFLUENCE_SITE_NAME=yourcompany
```

**Getting your Atlassian API Token:**
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label (e.g., "ConfluenceLens")
4. Copy the token immediately (you won't be able to see it again)

**Finding your site name:**
Your site name is the subdomain in your Confluence URL:
`https://[SITE_NAME].atlassian.net/wiki/...`

## Usage

### Running the Server

Start the MCP server:

```bash
python server.py
```

### Using the Tool

The server provides a `fetch_confluence_page` tool that accepts:

- `page_id` (required): The Confluence page ID
- `site_name` (optional): Override the default site name from environment variables

**Finding a page ID:**
The page ID is in the URL when viewing a Confluence page:
`https://yoursite.atlassian.net/wiki/spaces/SPACE/pages/[PAGE_ID]/Page+Title`

### Example

```python
# The MCP client will call the tool like this:
result = fetch_confluence_page(page_id="123456789")
```

The tool returns the page content in Markdown format with the title as an H1 header.

## Configuration for MCP Clients

Add this to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "confluencelens": {
      "command": "python",
      "args": ["path/to/confluencelens/server.py"],
      "env": {
        "ATLASSIAN_USER_EMAIL": "your.email@example.com",
        "ATLASSIAN_API_TOKEN": "your_api_token_here",
        "CONFLUENCE_SITE_NAME": "yourcompany"
      }
    }
  }
}
```

## Troubleshooting

### Authentication Errors

If you get 401 Unauthorized errors:
- Verify your API token is correct
- Ensure your email matches your Atlassian account
- Check that your token hasn't expired

### Page Not Found (404)

- Verify the page ID is correct
- Ensure you have permission to view the page
- Check that the site name is correct

### Connection Errors

- Verify your internet connection
- Check if Atlassian services are operational
- Ensure no firewall is blocking the connection

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

- 🐛 [Report bugs](https://github.com/yourusername/confluencelens/issues)
- 💡 [Request features](https://github.com/yourusername/confluencelens/issues)
- 💬 [Discussions](https://github.com/yourusername/confluencelens/discussions)

## Acknowledgments

Built with [FastMCP](https://github.com/jlowin/fastmcp) - A fast, Pythonic framework for building MCP servers.
