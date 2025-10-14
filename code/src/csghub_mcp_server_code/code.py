import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_list_codes,
    api_get_code_details
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

def register_code_tools(mcp_instance: FastMCP):
    register_code_list(mcp_instance=mcp_instance)
    register_code_query(mcp_instance=mcp_instance)

def register_code_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_user_codes",
        title="List codes for a user from CSGHub",
        description="Retrieve a list of codes for a specific user from CSGHub with user access token. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_user_codes(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()
        
        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        logger.info(f"Listing user codes for user: {username}")
        
        try:
            codes = api_list_codes(api_url, token, username, per, page)
            return json.dumps(codes)
        except Exception as e:
            logger.error(f"Error calling codes API: {e}")
            return f"Error: Failed to list codes. {e}"

def register_code_query(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_code_detail_by_path",
        title="Get code details by code path",
        description="Retrieve the code details by a specific path from CSGHub with user access token. This is useful for checking the details of a code repo that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_code_detail_by_path(token: str, code_path: str) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_get_code_details(api_url=api_url, token=token, code_path=code_path)
        return json.dumps({"data": json_data["data"]})
