import json
import logging
from mcp.server.fastmcp import FastMCP
from .api_client import (
    api_get_username_from_token,
    api_get_inference_status,
    api_list_inferences,
    api_inference_create,
    api_get_model_detail,
    api_get_available_resources,
    api_get_available_runtime_frameworks,
)
from .utils import (
    get_csghub_api_endpoint, 
    get_csghub_api_key
)

logger = logging.getLogger(__name__)

cluster_id = "ab45d3ba-a2ff-466e-887a-b2e5c0c070c5"

def register_inference_tools(mcp_instance: FastMCP):
    register_inference_list(mcp_instance=mcp_instance)
    register_inference_query(mcp_instance=mcp_instance)
    register_check_model(mcp_instance=mcp_instance)
    register_deploy_model_inference(mcp_instance=mcp_instance)
    query_available_resources_and_runtime_frameworks(mcp_instance=mcp_instance)
    
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
    
def register_deploy_model_inference(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="deploy_model_as_inference_by_model_id",
        title="Deploy model as inference service by model_id/runtime_framework_id/resource_id",
        description="Retrieve and find model detail and check if model exists in CSGHub by a specific deploy ID from CSGHub with user access token. User have to provide model_id, runtime_framework_id, resource_id to deploy model as inference service.",
        structured_output=True,
    )
    def deploy_model_as_inference_by_model_id(
        token: str,
        model_id: str,
        resource_id: int,
        runtime_framework_id: int,
    ) -> str:
        api_url = get_csghub_api_endpoint()
        
        json_data = api_inference_create(
            api_url=api_url,
            token=token,
            model_id=model_id,
            cluster_id=cluster_id,
            runtime_framework_id=runtime_framework_id,
            resource_id=resource_id,
        )
        return json.dumps({"data": json_data["data"]})

def query_available_resources_and_runtime_frameworks(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="query_available_resources_and_runtime_frameworks",
        title="Query available resources and runtime frameworks for deploying models",
        description="Retrieve a list of available resources and runtime frameworks that can be used for deploying models on CSGHub.",
        structured_output=True,
    )
    def query_available_resources_and_runtime_frameworks(model_id: str) -> str:
        api_url = get_csghub_api_endpoint()
        deploy_type = "1"
        res_json_data = api_get_available_resources(api_url, cluster_id, deploy_type)
        run_json_data = api_get_available_runtime_frameworks(api_url, model_id, deploy_type)

        return json.dumps({
            "resources_data": res_json_data["data"],
            "runtime_frameworks_data": run_json_data["data"]
        })
