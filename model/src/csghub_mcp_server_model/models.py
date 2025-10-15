import json
import logging
import requests
from mcp.server.fastmcp import FastMCP
from .api_client import (
    api_get_username_from_token,
    api_top_download_models,
    api_list_user_models,
    api_get_model_details,
    api_create_model,
)
from .utils import (
    get_csghub_api_endpoint,
    get_csghub_api_key,
)

logger = logging.getLogger(__name__)

def register_model_tools(mcp_instance: FastMCP):
    register_model_query_tools(mcp_instance=mcp_instance)
    register_user_model_list(mcp_instance=mcp_instance)
    register_model_query(mcp_instance=mcp_instance)
    register_model_creation(mcp_instance=mcp_instance)

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

def register_user_model_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_user_models",
        title="List models for a user from CSGHub",
        description="Retrieve a list of models for a specific user from CSGHub with user access token. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_user_models(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()
        
        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"
        
        try:
            models = api_list_user_models(api_url, token, username, per, page)
            return json.dumps(models)
        except Exception as e:
            logger.error(f"Error calling models API: {e}")
            return f"Error: Failed to list models. {e}"

def register_model_query(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_model_detail_by_path",
        title="Get model details by model path",
        description="Retrieve the model details by a specific path from CSGHub with user access token. This is useful for checking the details of a model repo that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_model_detail_by_path(token: str, model_path: str) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_get_model_details(api_url=api_url, token=token, model_path=model_path)
        return json.dumps({"data": json_data["data"]})

def register_model_creation(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="create_model",
        title="Create a new model repo in CSGHub with specified model name",
        description="Create a new model repo in CSGHub with user access token. This is useful for submitting a new model repo to the CSGHub service. model_name is required and must be must start with a letter, can only contain letters, numbers and special characters underscores (_) and hyphens (-). license and readme and description are optional. Default license is Apache-2.0. Default readme and description is empty.",
        structured_output=True,
    )
    def create_model(
        token: str,
        model_name: str, 
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

        json_data = api_create_model(
            api_url=api_url, 
            token=token,
            namespace=username,
            model_name=model_name,
            license=license,
            readme=readme,
            description=description,
        )
        
        access_url = f"https://opencsg.com/models/{username}/{model_name}"
        return json.dumps({"data": json_data["data"], "access_url": access_url})
