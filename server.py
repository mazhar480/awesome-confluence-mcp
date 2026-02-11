"""
ConfluenceLens MCP Server

A FastMCP server that fetches Confluence pages and converts them to Markdown.
"""

import os
from typing import Optional
import requests
from fastmcp import FastMCP
from html_to_markdown import convert

# Initialize FastMCP server
mcp = FastMCP("ConfluenceLens")

# Environment variables for authentication
ATLASSIAN_USER_EMAIL = os.getenv("ATLASSIAN_USER_EMAIL")
ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN")
SITE_NAME = os.getenv("CONFLUENCE_SITE_NAME")


@mcp.tool()
def fetch_confluence_page(page_id: str, site_name: Optional[str] = None) -> str:
    """
    Fetch a Confluence page and convert it to Markdown.
    
    Args:
        page_id: The Confluence page ID to fetch
        site_name: Optional site name override (defaults to CONFLUENCE_SITE_NAME env var)
    
    Returns:
        The page content converted to Markdown format
    
    Raises:
        ValueError: If required environment variables are not set
        requests.HTTPError: If the API request fails
    """
    # Validate environment variables
    if not ATLASSIAN_USER_EMAIL or not ATLASSIAN_API_TOKEN:
        raise ValueError(
            "Missing required environment variables: ATLASSIAN_USER_EMAIL and ATLASSIAN_API_TOKEN"
        )
    
    # Use provided site_name or fall back to environment variable
    confluence_site = site_name or SITE_NAME
    if not confluence_site:
        raise ValueError(
            "Site name must be provided either as parameter or CONFLUENCE_SITE_NAME environment variable"
        )
    
    # Construct the API URL
    url = f"https://{confluence_site}.atlassian.net/wiki/api/v2/pages/{page_id}?body-format=storage"
    
    # Make the API request with basic authentication
    response = requests.get(
        url,
        auth=(ATLASSIAN_USER_EMAIL, ATLASSIAN_API_TOKEN),
        headers={"Accept": "application/json"}
    )
    
    # Raise an exception for bad status codes
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    
    # Extract the page title and body
    title = data.get("title", "Untitled")
    body_html = data.get("body", {}).get("storage", {}).get("value", "")
    
    # Convert HTML to Markdown
    markdown_content = convert(body_html)
    
    # Format the output with title
    result = f"# {title}\n\n{markdown_content}"
    
    return result


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
