import logging
from src.csghub_mcp_server_space.main import app
from src.csghub_mcp_server_space.utils import constants

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # streamable-http
    # app(host='0.0.0.0', port=8000, protocol='streamable-http')
    # sse
    # app(host='0.0.0.0', port=8000, protocol='stdio')
    app(host='0.0.0.0', port=8000, protocol=constants.get_csghub_mcp_server_mode())
