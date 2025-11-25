import logging
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
    api_get_namespaces_by_token,
    api_list_datasets,
    api_get_dataset_details,
    api_create_dataset,
    api_delete_dataset,
    api_find_datasets_by_name,
    get_issue_data,
    upload_issue_data,
    api_create_dataset_new_branch,
    api_list_dataset_branchs,
)

logger = logging.getLogger(__name__)

def register_dataset_tools(mcp_instance: FastMCP):
    register_dataset_list(mcp_instance=mcp_instance)
    register_dataset_query(mcp_instance=mcp_instance)
    register_dataset_creation(mcp_instance=mcp_instance)
    register_dataset_delete(mcp_instance=mcp_instance)
    register_namespace_tools(mcp_instance=mcp_instance)
    register_dataset_query_tools(mcp_instance=mcp_instance)
    register_upload_issue_dataset(mcp_instance=mcp_instance)

def register_dataset_query_tools(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="query_datasets_by_name",
        title="Query datasets by name from CSGHub",
        description="Query the datasets from CSGHub by specifying dataset name. The default 20 datasets will be returned if no page size is specified. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def query_datasets_by_name(token: str, name: str, page: int = 1, page_size: int = 20) -> str:
       json_data = api_find_datasets_by_name(token=token, name=name, page=page, page_size=page_size)
       return json.dumps(json_data)

def register_dataset_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_user_datasets",
        title="List dataset repo for a user from CSGHub",
        description="Retrieve a list of dataset repo for a specific user from CSGHub with user access token. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_user_datasets(token: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        try:
            username = api_get_username_from_token(token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"
        
        try:
            datasets = api_list_datasets(token, username, per, page)
            return json.dumps(datasets)
        except Exception as e:
            logger.error(f"Error calling datasets API: {e}")
            return f"Error: Failed to list datasets. {e}"

def register_dataset_query(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="get_dataset_detail_by_id",
        title="Get dataset repo details by dataset path",
        description="Retrieve the dataset repo details by a specific path from CSGHub with user access token. This is useful for checking the details of a dataset repo that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_dataset_detail_by_id(token: str, dataset_id: str) -> str:
        json_data = api_get_dataset_details(token=token, dataset_id=dataset_id)
        return json.dumps(json_data)

def register_dataset_creation(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="create_dataset_repo",
        title="Create a new dataset repo in CSGHub with specified dataset name",
        description="Create a new dataset repo in CSGHub with user access token. This is useful for submitting a new dataset repo to the CSGHub service. dataset_name is required and must be must start with a letter, can only contain letters, numbers and special characters underscores (_) and hyphens (-). license and readme and description are optional. Default license is Apache-2.0. Default readme and description is empty.",
        structured_output=True,
    )
    def create_dataset_repo(
        token: str,
        dataset_name: str, 
        license: str = "apache-2.0",
        readme: str = "",
        description: str = "",
        namespace: str = None,
    ) -> str:
        if namespace is None or len(namespace.strip()) < 1:
            try:
                namespace = api_get_username_from_token(token)
            except Exception as e:
                logger.error(f"Error calling user token API: {e}")
                return f"Error: Failed to get username. {e}"

        json_data = api_create_dataset(
            token=token,
            namespace=namespace,
            dataset_name=dataset_name,
            license=license,
            readme=readme,
            description=description,
        )
        return json.dumps(json_data)

def register_dataset_delete(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="delete_dataset_by_id",
        title="Delete dataset repo by dataset id",
        description="Delete the dataset repo by a specific id from CSGHub with user access token.",
        structured_output=True,
    )
    def delete_dataset_by_id(token: str, dataset_id: str) -> str:
        json_data = api_delete_dataset(token=token, dataset_id=dataset_id)
        return json.dumps(json_data)

def register_namespace_tools(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_user_namespaces",
        title="List available namespaces or organizations for a user from CSGHub",
        description="Retrieve a list of namespaces or organizations that a user has access to create dataset repos from CSGHub with user access token.",
        structured_output=True,
    )
    def list_user_namespaces(token: str) -> str:
        namespaces = api_get_namespaces_by_token(token)
        return json.dumps(namespaces)

def register_upload_issue_dataset(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="upload_issue_latest_qa_to_dataset",
        title="Retrieve and upload csghub issue latest QA records to dataset.",
        description="Retrieve and upload csghub issue latest QA records to a branch of dataset on CSGHub with access token. The default branch is main. The default file name is records_vYYYYMMDD-HHMMSS.json to save.",
        structured_output=True,
    )
    def upload_issue_latest_qa_to_dataset(token: str, dataset_id: str, branch: str = "main", file_name: str = "") -> str:
        branches = api_list_dataset_branchs(token, dataset_id)
        if not isinstance(branches, list):
            return json.dumps(branches)
        
        if not branch in set(branches):
            new_branch = api_create_dataset_new_branch(token, dataset_id, branch)
            if "msg" not in new_branch or new_branch["msg"].lower() != "ok":
                return json.dumps(new_branch)
        
        records = []
        try:
            records = get_issue_data()
            if not isinstance(records, list):
                return json.dumps(records)
        except Exception as e:
            return f"Error: Failed to retrieve issue QA records - {e}"

        if len(records) < 1:
            return f"Error: No any issue records found."
        
        if file_name is None or file_name == "":
            file_name = f"records_v{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
            
        upload_result = upload_issue_data(token, dataset_id, branch, records, file_name)

        return json.dumps(upload_result)
