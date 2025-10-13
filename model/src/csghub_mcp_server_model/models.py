import json
import logging
import requests
from mcp.server.fastmcp import FastMCP
from .api_client import api_top_download_models
from .utils import get_csghub_api_endpoint

logger = logging.getLogger(__name__)

def register_model_tools(mcp_instance: FastMCP):
    register_model_query_tools(mcp_instance=mcp_instance)

def register_model_query_tools(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_top_download_models",
        title="Get top downloaded models from CSGHub",
        description="Retrieve the top downloaded models from CSGHub by specifying the number of models to retrieve.",
        structured_output=True,
    )
    def get_top_download_models(num: int) -> str:
       api_url = get_csghub_api_endpoint()
       json_data = api_top_download_models(api_url, num)
       return json.dumps({"data": json_data["data"]})
