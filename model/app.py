import sys
import os

from src.csghub_mcp_server_model.main import app

if __name__ == "__main__":
    # streamable-http
    app(host='0.0.0.0', port=8000, protocol='streamable-http')
    # sse
    # app(host='0.0.0.0', port=8000, protocol='sse')
