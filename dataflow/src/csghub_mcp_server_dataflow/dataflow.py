import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_list_jobs,
    api_get_job_details,
    api_create_job,
    api_delete_job,
    api_get_template_list,
    api_get_dataset_detail,
)

logger = logging.getLogger(__name__)

def register_dataflow_tools(mcp_instance: FastMCP):
    register_dataflow_list(mcp_instance=mcp_instance)
    register_dataflow_query(mcp_instance=mcp_instance)
    register_dataflow_create(mcp_instance=mcp_instance)
    register_dataflow_delete(mcp_instance=mcp_instance)
    register_dataflow_template_list(mcp_instance=mcp_instance)
    register_check_dataset(mcp_instance=mcp_instance)

def register_dataflow_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_user_dataflow_jobs",
        title="List dataflow jobs for a user from CSGHub with access token.",
        description="Retrieve a list of dataflow jobs for a specific user from CSGHub with user access token. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_user_dataflow_jobs(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        try:
            jobs = api_list_jobs(token, per, page)
            return json.dumps(jobs)
        except Exception as e:
            logger.error(f"Error calling dataflow API: {e}")
            return f"Error: Failed to list codes. {e}"

def register_dataflow_query(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_dataflow_job_detail_by_job_id",
        title="Get dataflow job details by job_id and template type",
        description="Retrieve the dataflow job details by a specific id and template type (default is 'data_refine') from CSGHub with user access token. This is useful for checking the details of a job that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_dataflow_job_detail_by_job_id(token: str, job_id: int, template_type: str = "data_refine") -> str:
        json_data = api_get_job_details(token=token, job_id=job_id, job_type=template_type)
        return json.dumps(json_data)

def register_dataflow_create(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="create_dataflow_job",
        title="Create a new dataflow job in CSGHub with specified parameters.",
        description="Create a new dataflow job in CSGHub with user access token. This is useful for submitting a new dataflow job to the CSGHub service. Please provide dataflow template infor such as template_id. All parameters except text_keys are required. The default value for text_keys is 'text' for column name of dataset. dataset_id is dataset id or path in CSGHub for the dataflow job to process. The default value for branch is 'main'.",
        structured_output=True,
    )
    def create_dataflow_job(
        token: str,
        dataset_id: str,
        template_id: int,
        branch: str = "main",
        text_keys: str = "text",
    ) -> str:
        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        json_data = api_create_job(
            token=token,
            template_id=template_id,
            dataset_id=dataset_id,
            branch=branch,
            username=username,
            text_keys=text_keys,
        )
        return json.dumps(json_data)

def register_dataflow_delete(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="delete_dataflow_job_by_id",
        title="Delete dataflow job by job id",
        description="Delete the dataflow job by a specific id from CSGHub with user access token.",
        structured_output=True,
    )
    def delete_dataflow_job_by_id(token: str, job_id: int) -> str:
        json_data = api_delete_job(token=token, job_id=job_id)
        return json.dumps(json_data)

def register_dataflow_template_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="query_dataflow_templates",
        title="Query available dataflow templates with access token.",
        description="Retrieve a list of available dataflow templates from CSGHub with user access token. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def query_dataflow_templates(token: str, page: int = 1, page_size: int = 20) -> str:
        json_data = api_get_template_list(token=token, page=page, page_size=page_size)
        return json.dumps(json_data)

def register_check_dataset(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="check_dataset_by_dataset_id",
        title="Get or search dataset detail and check dataset by dataset ID with token",
        description="Retrieve and find dataset detail and check if dataset exists in CSGHub by a specific ID from CSGHub.",
        structured_output=True,
    )
    def check_dataset_by_dataset_id(token: str, dataset_id: str) -> str:
        json_data = api_get_dataset_detail(token, dataset_id)
        return json.dumps(json_data)

