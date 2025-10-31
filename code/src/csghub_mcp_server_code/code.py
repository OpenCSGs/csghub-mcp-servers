import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_get_namespaces_by_token,
    api_list_codes,
    api_get_code_details,
    api_create_code,
    api_delete_code,
)

logger = logging.getLogger(__name__)

def register_code_tools(mcp_instance: FastMCP):
    register_code_list(mcp_instance=mcp_instance)
    register_code_query(mcp_instance=mcp_instance)
    register_code_creation(mcp_instance=mcp_instance)
    register_code_delete(mcp_instance=mcp_instance)
    register_namespace_tools(mcp_instance=mcp_instance)

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
        
        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        logger.info(f"Listing user codes for user: {username}")
        
        try:
            codes = api_list_codes(token, username, per, page)
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
    def get_code_detail_by_path(token: str, code_id: str) -> str:
        json_data = api_get_code_details(token=token, code_id=code_id)
        return json.dumps(json_data)

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
        namespace: str = None,
    ) -> str:
        if namespace is None or len(namespace.strip()) < 1:
            try:
                namespace = api_get_username_from_token(token)
            except Exception as e:
                logger.error(f"Error calling user token API: {e}")
                return f"Error: Failed to get username. {e}"

        json_data = api_create_code(
            token=token,
            namespace=namespace,
            code_name=code_name,
            license=license,
            readme=readme,
            description=description,
        )
        return json.dumps(json_data)

def register_code_delete(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="delete_code_by_id",
        title="Delete code repo by code id",
        description="Delete the code repo by a specific id from CSGHub with user access token.",
        structured_output=True,
    )
    def delete_code_by_path(token: str, code_id: str) -> str:
        json_data = api_delete_code(token=token, code_id=code_id)
        return json.dumps(json_data)

def register_namespace_tools(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_namespaces",
        title="List available namespaces or organizations for a user from CSGHub",
        description="Retrieve a list of namespaces or organizations that a user has access to create code repos from CSGHub with user access token.",
        structured_output=True,
    )
    def list_namespaces(token: str) -> str:
        namespaces = api_get_namespaces_by_token(token)
        return json.dumps(namespaces)
