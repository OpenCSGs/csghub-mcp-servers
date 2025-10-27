import json
import logging
from mcp.server.fastmcp import FastMCP
from .api_client import (
    api_get_username_from_token,
    api_top_download_models,
    api_list_user_models,
    api_get_model_details,
    api_create_model,
    api_delete_model,
)

logger = logging.getLogger(__name__)

def register_model_tools(mcp_instance: FastMCP):
    register_model_query_tools(mcp_instance=mcp_instance)
    register_user_model_list(mcp_instance=mcp_instance)
    register_model_query(mcp_instance=mcp_instance)
    register_model_creation(mcp_instance=mcp_instance)
    register_model_delete(mcp_instance=mcp_instance)

def register_model_query_tools(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_top_download_models",
        title="Get top downloaded models from CSGHub",
        description="Retrieve the top downloaded models from CSGHub by specifying the number of models to retrieve.",
        structured_output=True,
    )
    def get_top_download_models(num: int) -> str:
       json_data = api_top_download_models(num)
       return json.dumps(json_data)

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
        
        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"
        
        try:
            models = api_list_user_models(token, username, per, page)
            return json.dumps(models)
        except Exception as e:
            logger.error(f"Error calling models API: {e}")
            return f"Error: Failed to list models. {e}"

def register_model_query(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_model_detail_by_id",
        title="Get model details by model id",
        description="Retrieve the model details by a specific ID or path from CSGHub with user access token. This is useful for checking the details of a model repo that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_model_detail_by_id(token: str, model_id: str) -> str:
        json_data = api_get_model_details(token=token, model_id=model_id)
        return json.dumps(json_data)

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

        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        json_data = api_create_model(
            token=token,
            namespace=username,
            model_name=model_name,
            license=license,
            readme=readme,
            description=description,
        )
        
        return json.dumps(json_data)

def register_model_delete(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="delete_model_by_id",
        title="Delete model repo by model id",
        description="Delete the model repo by a specific id from CSGHub with user access token.",
        structured_output=True,
    )
    def delete_model_by_id(token: str, model_id: str) -> str:
        json_data = api_delete_model(token=token, model_id=model_id)
        return json.dumps(json_data)
