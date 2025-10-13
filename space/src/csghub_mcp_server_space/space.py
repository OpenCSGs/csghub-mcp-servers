import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_get_top_download_spaces,
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

def register_space_tools(mcp_instance: FastMCP):
    pass