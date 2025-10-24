import logging
import json
from mcp.server.fastmcp import FastMCP

from .api_client import (
    api_get_username_from_token,
    api_list_finetunes,
    api_get_finetune_status,
    api_finetune_create,
    api_finetune_stop,
    api_finetune_start,
    api_finetune_delete,
    api_get_available_resources,
    api_get_available_runtime_frameworks,
    api_get_model_detail,
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
    register_finetune_control_tools(mcp_instance=mcp_instance)
    register_check_model(mcp_instance=mcp_instance)

def register_finetune_list(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="list_finetune_instance",
        title="List finetune instance with UI for a user from CSGHub with user access token",
        description="Retrieve a list of finetune instance with UI for a specific user from CSGHub. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_finetune_instance(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        api_key = get_csghub_api_key()
        
        try:
            username = api_get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        logger.info(f"Listing finetune jobs for user: {username}")
        
        try:
            finetunes = api_list_finetunes(api_url, token, username, per, page)
            return json.dumps(finetunes)
        except Exception as e:
            logger.error(f"Error calling finetune API: {e}")
            return f"Error: Failed to list finetune services. {e}"

def register_finetune_query(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="get_finetune_status_by_id",
        title="Get Finetune deployment details and status by job ID",
        description="Retrieve the finetune job details and status by using a specific ID from CSGHub with user access token. This is useful for checking the status of a deployed model's finetune job.",
        structured_output=True,
    )
    def get_finetuen_status_by_id(token: str, model_id: str, deploy_id: int) -> str:
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

def register_finetune_control_tools(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="stop_finetune_by_modelid_and_deployid",
        title="Stop an deployed finetune service by model id and deploy id and finetune status should be stopped",
        description="Stop an running finetune service by model id and deploy id on CSGHub with user access token. model id and deploy id are required to stop the finetune service.",
        structured_output=True,
    )
    def stop_finetune_by_modelid_and_deployid(token: str, model_id: str, deploy_id: int) -> str:
        api_url = get_csghub_api_endpoint()
        res_json_data = api_finetune_stop(api_url, token, model_id, deploy_id)
        return json.dumps(res_json_data)

    @mcp_instance.tool(
        name="start_finetune_by_modelid_and_deployid",
         title="Start an deployed finetune service by model id and deploy id and finetune status should be running",
        description="Start an stopped finetune service by model id and deploy id on CSGHub with user access token. model id and deploy id are required to start the finetune service.",
        structured_output=True,
    )
    def start_finetune_by_modelid_and_deployid(token: str, model_id: str, deploy_id: int) -> str:
        api_url = get_csghub_api_endpoint()
        res_json_data = api_finetune_start(api_url, token, model_id, deploy_id)
        return json.dumps(res_json_data)
    
    @mcp_instance.tool(
        name="delete_finetune_by_modelid_and_deployid",
         title="Delete an deployed finetune service by model id and deploy id",
        description="Delete an finetune service by model id and deploy id on CSGHub with user access token. model id and deploy id are required to delete the finetune service. It's good idea to stop finetune service before deleting it.",
        structured_output=True,
    )
    def delete_finetune_by_modelid_and_deployid(token: str, model_id: str, deploy_id: int) -> str:
        api_url = get_csghub_api_endpoint()
        res_json_data = api_finetune_delete(api_url, token, model_id, deploy_id)
        return json.dumps(res_json_data)  

def register_check_model(mcp_instance: FastMCP):
    
    @mcp_instance.tool(
        name="check_model_by_model_id",
        title="Get or search model detail and check model by model ID",
        description="Retrieve and find model detail and check if model exists in CSGHub by a specific deploy ID from CSGHub.",
        structured_output=True,
    )
    def check_model_by_model_id(model_id: str) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = api_get_model_detail(api_url, model_id)
        return json.dumps({"data": json_data["data"]})

