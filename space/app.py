import logging
from src.csghub_mcp_server_space.main import app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # streamable-http
    # app(host='0.0.0.0', port=8000, protocol='streamable-http')
    # sse
    app(host='0.0.0.0', port=8000, protocol='sse')
