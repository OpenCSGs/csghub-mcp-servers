import logging
import json
from mcp.server.fastmcp import FastMCP

from .api_client import (
    api_get_username_from_token,
    api_list_finetunes,
    api_get_finetune_status,
    api_finetune_create,
    api_get_available_resources,
    api_get_available_runtime_frameworks,
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

cluster_id = "ab45d3ba-a2ff-466e-887a-b2e5c0c070c5"

def register_finetune_tools(mcp_instance: FastMCP):
    register_finetune_list(mcp_instance=mcp_instance)
    register_finetune_query(mcp_instance=mcp_instance)
    register_query_finetune_conditions(mcp_instance=mcp_instance)
    register_finetune_create(mcp_instance=mcp_instance)

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
        response_data = api_get_finetune_status(api_url, token, model_id, deploy_id)
        json_data = response_data["data"]
        access_url = ""
        status = json_data["status"]
        deploy_name = json_data["deploy_name"]
        if status.lower() == "running":
            access_url = f"https://opencsg.com/finetune/{model_id}/{deploy_name}/{deploy_id}?tab=pages"
        return json.dumps({"data": json_data, "access_url": access_url})

def register_query_finetune_conditions(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="query_available_resources_and_runtime_frameworks_for_finetune",
        title="Query available resources and runtime frameworks for deploying finetune service",
        description="Retrieve a list of available resources and runtime frameworks that can be used for deploying finetune service on CSGHub.",
        structured_output=True,
    )
    def query_available_resources_and_runtime_frameworks_for_finetune(model_id: str) -> str:
        api_url = get_csghub_api_endpoint()
        deploy_type = "2"
        res_json_data = api_get_available_resources(api_url, cluster_id, deploy_type)
        run_json_data = api_get_available_runtime_frameworks(api_url, model_id, deploy_type)

        return json.dumps({
            "resources_data": res_json_data["data"],
            "runtime_frameworks_data": run_json_data["data"]
        })

def register_finetune_create(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="deploy_finetune_by_model_id",
        title="Deploy finetune service by model_id/runtime_framework_id/resource_id",
        description="Deploy finetune service by a specific model ID from CSGHub with user access token. User have to provide model_id, runtime_framework_id, resource_id to deploy finetune service.",
        structured_output=True,
    )
    def deploy_finetune_by_model_id(
        token: str,
        model_id: str,
        resource_id: int,
        runtime_framework_id: int,
    ) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_finetune_create(
            api_url=api_url,
            token=token,
            model_id=model_id,
            cluster_id=cluster_id,
            runtime_framework_id=runtime_framework_id,
            resource_id=resource_id,
        )
        return json.dumps({"data": json_data["data"]})
