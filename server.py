#!/usr/bin/env python3
"""
Awesome Confluence MCP Server
A token-efficient MCP server for Confluence integration with Markdown conversion.
"""

import os
import logging
from typing import Any, Optional
from dotenv import load_dotenv
import requests
from markdownify import markdownify as md
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("awesome-confluence-mcp")

# Confluence API configuration
CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", "").rstrip("/")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL", "")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN", "")

# Validate configuration
if not all([CONFLUENCE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN]):
    logger.warning(
        "Confluence credentials not fully configured. "
        "Please set CONFLUENCE_URL, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN in .env file."
    )


class ConfluenceClient:
    """Client for interacting with Confluence Cloud REST API."""
    
    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url
        self.auth = (email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make HTTP request to Confluence API with error handling."""
        url = f"{self.base_url}/wiki/rest/api{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                auth=self.auth,
                headers=self.headers,
                timeout=30,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise Exception(f"Confluence API error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error occurred: {e}")
            raise Exception(f"Failed to connect to Confluence: {str(e)}")
    
    def list_spaces(self, limit: int = 25) -> list[dict]:
        """List all accessible Confluence spaces."""
        params = {
            "limit": limit,
            "type": "global"
        }
        response = self._make_request("GET", "/space", params=params)
        return response.get("results", [])
    
    def search_pages(
        self, 
        query: str, 
        space_key: Optional[str] = None, 
        limit: int = 10
    ) -> list[dict]:
        """Search for Confluence pages by title or content."""
        cql = f'type=page and (title~"{query}" or text~"{query}")'
        if space_key:
            cql += f' and space="{space_key}"'
        
        params = {
            "cql": cql,
            "limit": limit,
            "expand": "space,version"
        }
        response = self._make_request("GET", "/content/search", params=params)
        return response.get("results", [])
    
    def get_page_content(self, page_id: str) -> dict:
        """Fetch a specific page with its content."""
        params = {
            "expand": "body.storage,space,version,metadata.labels"
        }
        return self._make_request("GET", f"/content/{page_id}", params=params)


# Initialize Confluence client
confluence = ConfluenceClient(CONFLUENCE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)


@mcp.tool()
def list_spaces(limit: int = 25) -> str:
    """
    List all Confluence spaces accessible to the authenticated user.
    
    Args:
        limit: Maximum number of spaces to return (default: 25, max: 100)
    
    Returns:
        JSON string containing space information including keys, names, and types
    """
    try:
        if limit < 1 or limit > 100:
            return "Error: limit must be between 1 and 100"
        
        spaces = confluence.list_spaces(limit=limit)
        
        # Format response
        result = {
            "total": len(spaces),
            "spaces": [
                {
                    "key": space.get("key"),
                    "name": space.get("name"),
                    "type": space.get("type"),
                    "id": space.get("id"),
                    "url": f"{CONFLUENCE_URL}/wiki/spaces/{space.get('key')}"
                }
                for space in spaces
            ]
        }
        
        import json
        return json.dumps(result, indent=2)
    
    except Exception as e:
        logger.error(f"Error listing spaces: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def search_pages(query: str, space_key: Optional[str] = None, limit: int = 10) -> str:
    """
    Search for Confluence pages by title or content.
    
    Args:
        query: Search query string to match against page titles and content
        space_key: Optional space key to limit search to a specific space
        limit: Maximum number of results to return (default: 10, max: 50)
    
    Returns:
        JSON string containing matching pages with titles, IDs, spaces, and URLs
    """
    try:
        if not query or not query.strip():
            return "Error: query parameter is required and cannot be empty"
        
        if limit < 1 or limit > 50:
            return "Error: limit must be between 1 and 50"
        
        pages = confluence.search_pages(query=query, space_key=space_key, limit=limit)
        
        # Format response
        result = {
            "total": len(pages),
            "query": query,
            "space_key": space_key,
            "pages": [
                {
                    "id": page.get("id"),
                    "title": page.get("title"),
                    "type": page.get("type"),
                    "space": {
                        "key": page.get("space", {}).get("key"),
                        "name": page.get("space", {}).get("name")
                    },
                    "version": page.get("version", {}).get("number"),
                    "url": f"{CONFLUENCE_URL}/wiki{page.get('_links', {}).get('webui', '')}"
                }
                for page in pages
            ]
        }
        
        import json
        return json.dumps(result, indent=2)
    
    except Exception as e:
        logger.error(f"Error searching pages: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def fetch_page_markdown(page_id: str) -> str:
    """
    Fetch a Confluence page and convert it to Markdown format.
    
    This tool retrieves page content and converts it from HTML to Markdown,
    reducing token usage by 60-80% compared to raw HTML while preserving
    formatting, links, and structure.
    
    Args:
        page_id: The Confluence page ID to fetch
    
    Returns:
        Markdown-formatted page content with metadata header
    """
    try:
        if not page_id or not page_id.strip():
            return "Error: page_id parameter is required and cannot be empty"
        
        # Fetch page content
        page = confluence.get_page_content(page_id)
        
        # Extract metadata
        title = page.get("title", "Untitled")
        space_key = page.get("space", {}).get("key", "")
        space_name = page.get("space", {}).get("name", "")
        version = page.get("version", {}).get("number", 1)
        page_url = f"{CONFLUENCE_URL}/wiki{page.get('_links', {}).get('webui', '')}"
        
        # Extract HTML content
        html_content = page.get("body", {}).get("storage", {}).get("value", "")
        
        if not html_content:
            return f"Error: No content found for page ID {page_id}"
        
        # Convert HTML to Markdown
        markdown_content = md(
            html_content,
            heading_style="ATX",
            bullets="-",
            strip=['script', 'style']
        )
        
        # Extract labels if available
        labels = page.get("metadata", {}).get("labels", {}).get("results", [])
        label_names = [label.get("name") for label in labels if label.get("name")]
        
        # Format final output with metadata
        output = f"""# {title}

**Space:** {space_name} ({space_key})  
**Version:** {version}  
**URL:** {page_url}
"""
        
        if label_names:
            output += f"**Labels:** {', '.join(label_names)}\n"
        
        output += f"\n---\n\n{markdown_content}"
        
        return output
    
    except Exception as e:
        logger.error(f"Error fetching page {page_id}: {e}")
        return f"Error: {str(e)}"


def main():
    """Run the MCP server."""
    logger.info("Starting Awesome Confluence MCP Server...")
    logger.info(f"Confluence URL: {CONFLUENCE_URL}")
    
    if not all([CONFLUENCE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN]):
        logger.error(
            "Missing required environment variables. "
            "Please configure CONFLUENCE_URL, CONFLUENCE_EMAIL, and CONFLUENCE_API_TOKEN."
        )
        return
    
    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
