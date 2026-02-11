# Python runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY server.py .
COPY README.md .
COPY LICENSE .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Set environment variables (these will be overridden by user configuration)
ENV CONFLUENCE_URL=""
ENV CONFLUENCE_EMAIL=""
ENV CONFLUENCE_API_TOKEN=""

# Expose MCP server
CMD ["python", "-m", "server"]
