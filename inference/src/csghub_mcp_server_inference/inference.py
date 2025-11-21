import json
import logging
import os
from mcp.server.fastmcp import FastMCP
from .api_client import (
    api_get_username_from_token,
    api_get_inference_status,
    api_list_inferences,
    api_inference_create,
    api_get_model_detail,
    api_get_available_resources,
    api_get_available_runtime_frameworks,
    api_get_model_quantizations_list,
    api_inference_stop,
    api_inference_start,
    api_inference_delete,
)

logger = logging.getLogger(__name__)

def register_inference_tools(mcp_instance: FastMCP):
    register_inference_list(mcp_instance=mcp_instance)
    register_inference_query(mcp_instance=mcp_instance)
    register_check_model(mcp_instance=mcp_instance)
    register_deploy_model_inference(mcp_instance=mcp_instance)
    register_query_inference_conditions(mcp_instance=mcp_instance)
    register_inference_control_tools(mcp_instance=mcp_instance)
    
def register_inference_list(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="list_inference_services",
        title="List inference services for a user from CSGHub",
        description="Retrieve a list of inference services for a specific user from CSGHub. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_inference(token: str, per: int = 50, page: int = 1) -> str:
        if not token:
            return "error: must input CSGHUB_ACCESS_TOKEN."
        
        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"error calling user token API: {e}")
            return f"error: Failed to get username. {e}"

        logger.info(f"Listing inference services for user: {username}")
        
        try:
            inferences = api_list_inferences(token, username, per, page)
            return json.dumps(inferences)
        except Exception as e:
            logger.error(f"error calling inference API: {e}")
            return f"error: Failed to list inference services. {e}"

def register_inference_query(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_inference_status_by_deploy_id",
        title="Get Inference deployment details and status by model ID and deploy ID",
        description="Retrieve the inference deployment details and status by using model ID and a specific deploy ID from CSGHub with user access token. This is useful for checking the status of a deployed model's inference service.",
        structured_output=True,
    )
    def get_inference_status_by_deploy_id(token: str, model_id: str, deploy_id: int) -> str:
        json_data = api_get_inference_status(token, model_id, deploy_id)
        return json.dumps(json_data)

def register_check_model(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="check_model_by_model_id",
        title="Get or search model detail and check model by model ID",
        description="Retrieve and find model detail and check if model exists in CSGHub by a specific deploy ID from CSGHub.",
        structured_output=True,
    )
    def check_model_by_model_id(model_id: str) -> str:
        json_data = api_get_model_detail(model_id)
        return json.dumps(json_data)
    
def register_deploy_model_inference(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="deploy_model_as_inference_by_model_id",
        title="Deploy model as inference service by model_id/runtime_framework_id/resource_id",
        description="Deploy model as inference service by a specific model_id from CSGHub with user access token. User have to provide model_id, runtime_framework_id, resource_id to deploy model as inference service. gguf_quantization_name is optional and only required for GGUF model. The parameter agent is optional and can be used to specify the agent configuration for inference.",
        structured_output=True,
    )
    def deploy_model_as_inference_by_model_id(
        token: str,
        model_id: str,
        cluster_id: str,
        resource_id: int,
        runtime_framework_id: int,
        gguf_quantization_name: str = "",
        agent: str = "",
    ) -> str:
        json_data = api_inference_create(
            token=token,
            model_id=model_id,
            cluster_id=cluster_id,
            runtime_framework_id=runtime_framework_id,
            resource_id=resource_id,
            entrypoint=gguf_quantization_name,
            agent=agent,
        )
        return json.dumps(json_data)

def register_query_inference_conditions(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="query_available_resources_and_runtime_frameworks_for_inference",
        title="Query available resources and runtime frameworks for deploying model as inference service with user access token.",
        description="Retrieve a list of available resources and runtime frameworks that can be used for deploying model as inference on CSGHub. Retrieve gguf quantization list for model id of GGUF model.",
        structured_output=True,
    )
    def query_available_resources_and_runtime_frameworks_for_inference(token: str, model_id: str) -> str:
        deploy_type = "1"
        res_json_data = api_get_available_resources(token, deploy_type)
        run_json_data = api_get_available_runtime_frameworks(model_id, deploy_type)
        gguf_json_data = api_get_model_quantizations_list(model_id)
        return json.dumps({
            "resources_data": res_json_data,
            "runtime_frameworks_data": run_json_data,
            "gguf_quantizations_data": gguf_json_data,
        })

def register_inference_control_tools(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="stop_inference_by_modelid_and_deployid",
        title="Stop an deployed inference service by model id and deploy id and inference status should be stopped",
        description="Stop an running inference service by model id and deploy id on CSGHub with user access token. model id and deploy id are required to stop the inference service.",
        structured_output=True,
    )
    def stop_inference_by_modelid_and_deployid(token: str, model_id: str, deploy_id: int) -> str:
        res_json_data = api_inference_stop(token, model_id, deploy_id)
        return json.dumps(res_json_data)

    @mcp_instance.tool(
        name="start_inference_by_modelid_and_deployid",
         title="Start an deployed inference service by model id and deploy id and inference status should be running",
        description="Start an stopped inference service by model id and deploy id on CSGHub with user access token. model id and deploy id are required to start the inference service.",
        structured_output=True,
    )
    def start_inference_by_modelid_and_deployid(token: str, model_id: str, deploy_id: int) -> str:
        res_json_data = api_inference_start(token, model_id, deploy_id)
        return json.dumps(res_json_data)
    
    @mcp_instance.tool(
        name="delete_inference_by_modelid_and_deployid",
         title="Delete an deployed inference service by model id and deploy id",
        description="Delete an inference service by model id and deploy id on CSGHub with user access token. model id and deploy id are required to delete the inference service. It's good idea to stop the inference service before deleting it.",
        structured_output=True,
    )
    def delete_inference_by_modelid_and_deployid(token: str, model_id: str, deploy_id: int) -> str:
        res_json_data = api_inference_delete(token, model_id, deploy_id)
        return json.dumps(res_json_data)

