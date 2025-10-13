import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_list_finetunes,
    api_get_finetune_status
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

def register_finetune_tools(mcp_instance: FastMCP):
    register_finetune_list(mcp_instance=mcp_instance)
    register_finetune_query(mcp_instance=mcp_instance)

def register_finetune_list(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="list_finetune_services",
        title="List finetune services for a user from CSGHub",
        description="Retrieve a list of finetune services for a specific user from CSGHub. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_finetune(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()
        
        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        logger.info(f"Listing finetune services for user: {username}")
        
        try:
            finetunes = api_list_finetunes(api_url, token, username, per, page)
            return json.dumps(finetunes)
        except Exception as e:
            logger.error(f"Error calling finetune API: {e}")
            return f"Error: Failed to list finetune services. {e}"

def register_finetune_query(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="get_finetune_status_by_deploy_id",
        title="Get Finetune deployment details and status by model ID and deploy ID",
        description="Retrieve the finetune deployment details and status by using model ID and a specific deploy ID from CSGHub with user access token. This is useful for checking the status of a deployed model's finetune instance service.",
        structured_output=True,
    )
    def get_finetuen_status_by_deploy_id(token: str, model_id: str, deploy_id: int) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_get_finetune_status(api_url, token, model_id, deploy_id)
        return json.dumps({"data": json_data["data"]})
