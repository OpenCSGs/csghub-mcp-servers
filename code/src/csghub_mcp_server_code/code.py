import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_list_codes,
    api_get_code_details,
    api_create_code,
    api_delete_code,
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

def register_code_tools(mcp_instance: FastMCP):
    register_code_list(mcp_instance=mcp_instance)
    register_code_query(mcp_instance=mcp_instance)
    register_code_creation(mcp_instance=mcp_instance)
    register_code_delete(mcp_instance=mcp_instance)

def register_code_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_user_codes",
        title="List code repo for a user from CSGHub",
        description="Retrieve a list of code repo for a specific user from CSGHub with user access token. You can control the pagination by specifying the number of items per page and the page number.",
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
        title="Get code repo details by code path",
        description="Retrieve the code repo details by a specific path from CSGHub with user access token. This is useful for checking the details of a code repo that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_code_detail_by_path(token: str, code_path: str) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_get_code_details(api_url=api_url, token=token, code_path=code_path)
        return json.dumps({"data": json_data["data"]})

def register_code_creation(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="create_code",
        title="Create a new code repo in CSGHub with specified code name",
        description="Create a new code repo in CSGHub with user access token. This is useful for submitting a new code repo to the CSGHub service. code_name is required and must be must start with a letter, can only contain letters, numbers and special characters underscores (_) and hyphens (-). license and readme and description are optional. Default license is Apache-2.0. Default readme and description is empty.",
        structured_output=True,
    )
    def create_code(
        token: str,
        code_name: str, 
        license: str = "apache-2.0",
        readme: str = "",
        description: str = "",
    ) -> str:
        api_key = get_csghub_api_key()
        api_url = get_csghub_api_endpoint()

        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        json_data = api_create_code(
            api_url=api_url, 
            token=token,
            namespace=username,
            code_name=code_name,
            license=license,
            readme=readme,
            description=description,
        )
        access_url = f"https://opencsg.com/codes/{username}/{code_name}"
        return json.dumps({"data": json_data["data"], "access_url": access_url})

def register_code_delete(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="delete_code_by_path",
        title="Delete code repo by code path",
        description="Delete the code repo by a specific path from CSGHub with user access token.",
        structured_output=True,
    )
    def delete_code_by_path(token: str, code_path: str) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_delete_code(api_url=api_url, token=token, code_path=code_path)
        return json.dumps(json_data)

