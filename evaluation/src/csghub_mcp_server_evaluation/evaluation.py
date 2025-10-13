import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_list_evaluations,
    api_get_evaluation_details
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

def register_evaluation_tools(mcp_instance: FastMCP):
    register_evaluation_list(mcp_instance=mcp_instance)
    register_evaluation_query(mcp_instance=mcp_instance)

def register_evaluation_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_evaluation_services",
        title="List evaluation services for a user from CSGHub",
        description="Retrieve a list of evaluation services for a specific user from CSGHub. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_evaluation(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()
        
        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        logger.info(f"Listing evaluation services for user: {username}")
        
        try:
            evaluations = api_list_evaluations(api_url, token, username, per, page)
            return json.dumps(evaluations)
        except Exception as e:
            logger.error(f"Error calling evaluation API: {e}")
            return f"Error: Failed to list evaluation services. {e}"

def register_evaluation_query(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="get_evaluation_by_id",
        title="Get evaluation details by numeric ID",
        description="Retrieve the evaluation details by a specific numeric ID from CSGHub with user access token. This is useful for checking the details of a evaluation that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_evaluation_by_id(token: str, id: int) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_get_evaluation_details(api_url, token, id)
        return json.dumps({"data": json_data["data"]})
