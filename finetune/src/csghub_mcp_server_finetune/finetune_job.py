import logging
import json
import os
from mcp.server.fastmcp import FastMCP

from .api_client import (
    api_get_username_from_token,
    api_get_available_resources,
    api_get_available_runtime_frameworks_by_deploy_type,
    api_get_model_detail,
    api_get_dataset_detail,
    api_list_finetune_jobs,
    api_get_finetune_job,
    api_delete_finetune_job,
    api_create_finetune_job,
    api_query_finetune_job_logs,
)

logger = logging.getLogger(__name__)

cluster_id = os.getenv("CLUSTER_ID", "ab45d3ba-a2ff-466e-887a-b2e5c0c070c5")

def register_finetune_job_tools(mcp_instance: FastMCP):
    register_finetune_job_list(mcp_instance=mcp_instance)
    register_finetune_job_control(mcp_instance=mcp_instance)
    register_query_finetune_job_conditions(mcp_instance=mcp_instance)
    register_finetune_job_create(mcp_instance=mcp_instance)
    register_check_model_dataset(mcp_instance=mcp_instance)

def register_finetune_job_list(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="list_finetune_jobs",
        title="List finetune jobs for a user from CSGHub with user access token",
        description="Retrieve a list of finetune jobs for a specific user from CSGHub. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_finetune_jobs(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        logger.info(f"Listing finetune jobs for user: {username}")
        
        try:
            finetunes = api_list_finetune_jobs(token, username, per, page)
            return json.dumps(finetunes)
        except Exception as e:
            logger.error(f"Error calling finetune API: {e}")
            return f"Error: Failed to list finetune services. {e}"

def register_finetune_job_control(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_finetune_job_by_id",
        title="Get Finetune job details and status by job ID",
        description="Retrieve the finetune job details and status by using a specific ID from CSGHub with user access token. This is useful for checking the status of a deployed finetune job.",
        structured_output=True,
    )
    def get_finetune_job_by_id(token: str, id: int) -> str:
        response_data = api_get_finetune_job(token, id)
        return json.dumps(response_data)
    
    @mcp_instance.tool(
        name="delete_finetune_job_by_id",
        title="Delete Finetune job by job ID",
        description="Delete the finetune jobby using a specific ID from CSGHub with user access token.",
        structured_output=True,
    )
    def delete_finetune_job_by_id(token: str, id: int) -> str:
        response_data = api_delete_finetune_job(token, id)
        return json.dumps(response_data)
    
    @mcp_instance.tool(
        name="api_query_finetune_job_logs",
        title="Get Finetune job logs by job ID",
        description="Retrieve the finetune job logs by using a specific ID from CSGHub with user access token. This is useful for checking failure reasion and process details of finetune job. Parameter since can be one of 10mins, 30mins, 1hour, 6hours, 1day, 2days, 1week, and default is all.",
        structured_output=True,
    )
    def get_finetune_job_logs_by_id(token: str, job_id: int, since = "all") -> str:
        response_data = api_query_finetune_job_logs(token=token, job_id=job_id, since=since)
        return json.dumps(response_data)


def register_query_finetune_job_conditions(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="query_avai_res_and_frameworks_for_finetune_job",
        title="Query available resources and runtime frameworks for deploying finetune job with user token",
        description="Retrieve a list of available resources and runtime frameworks that can be used for deploying finetune job on CSGHub. Only using GPU resources.",
        structured_output=True,
    )
    def query_avai_res_and_frameworks_for_finetune_job(token: str) -> str:
        deploy_type = "6"
        res_json_data = api_get_available_resources(cluster_id, deploy_type)
        run_json_data = api_get_available_runtime_frameworks_by_deploy_type(token, deploy_type)

        return json.dumps({
            "resources_data": res_json_data,
            "runtime_frameworks_data": run_json_data
        })

def register_finetune_job_create(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="deploy_finetune_job",
        title="Deploy finetune job by model_id/dataset_id/runtime_framework_id/resource_id",
        description="Deploy finetune job by a specific model ID and dataset ID from CSGHub with user access token. User have to provide model_id, dataset_id, runtime_framework_id, resource_id to deploy finetune service, epochs and learning rate are optional parameters. GPU resources are required. The parameter agents is optional and can be used to specify the agent configuration for the finetune job.",
        structured_output=True,
    )
    def deploy_finetune_job(
        token: str,
        model_id: str, dataset_id: str,
        resource_id: int, runtime_framework_id: int,
        epochs: int = 1, learning_rate: float = 0.0001,
        agents: str = "",
    ) -> str:
        json_data = api_get_model_detail(token, model_id)
        if "model_id" not in json_data:
            return json.dumps({"error": "Model not found. Please check the model ID."})
        
        json_data = api_get_dataset_detail(token, dataset_id)
        if "dataset_id" not in json_data:
            return json.dumps({"error": "Dataset not found. Please check the dataset ID."})
        
        json_data = api_create_finetune_job(
            token=token,
            model_id=model_id,
            dataset_id=dataset_id,
            rf_id=runtime_framework_id,
            res_id=resource_id,
            epochs=epochs,
            learning_rate=learning_rate,
            agents=agents,
        )
        return json.dumps(json_data)

def register_check_model_dataset(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="check_model_by_model_id",
        title="Get or search model detail and check model by model ID with token",
        description="Retrieve and find model detail and check if model exists in CSGHub by a specific ID from CSGHub.",
        structured_output=True,
    )
    def check_model_by_model_id(token: str, model_id: str) -> str:
        json_data = api_get_model_detail(token, model_id)
        return json.dumps(json_data)

    @mcp_instance.tool(
        name="check_dataset_by_dataset_id",
        title="Get or search dataset detail and check dataset by dataset ID with token",
        description="Retrieve and find dataset detail and check if dataset exists in CSGHub by a specific ID from CSGHub.",
        structured_output=True,
    )
    def check_dataset_by_dataset_id(token: str, dataset_id: str) -> str:
        json_data = api_get_dataset_detail(token, dataset_id)
        return json.dumps(json_data)

