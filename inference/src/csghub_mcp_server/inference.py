import json
import logging
from mcp.server.fastmcp import FastMCP
from .api_client import (
    api_get_username_from_token,
    api_get_inference_status,
    api_list_inferences
)
from .utils import get_csghub_api_endpoint, get_csghub_api_key

logger = logging.getLogger(__name__)

def register_inference_tools(mcp_instance: FastMCP):
    register_inference_list(mcp_instance=mcp_instance)
    register_inference_query(mcp_instance=mcp_instance)
    
def register_inference_list(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="list_inference_services",
        title="List inference services for a user from CSGHub",
        description="Retrieve a list of inference services for a specific user from CSGHub. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_inference(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()
        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        logger.info(f"Listing inference services for user: {username}")
        
        try:
            inferences = api_list_inferences(api_url, token, username, per, page)
            return json.dumps(inferences)
        except Exception as e:
            logger.error(f"Error calling inference API: {e}")
            return f"Error: Failed to list inference services. {e}"

def register_inference_query(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_inference_status_by_deploy_id",
        title="Get Inference deployment details and status by model ID and deploy ID",
        description="Retrieve the inference deployment details and status by using model ID and a specific deploy ID from CSGHub with user access token. This is useful for checking the status of a deployed model's inference service.",
        structured_output=True,
    )
    def get_inference_status_by_deploy_id(token: str, model_id: str, deploy_id: int) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_get_inference_status(api_url, token, model_id, deploy_id)
        return json.dumps({"data": json_data["data"]})
