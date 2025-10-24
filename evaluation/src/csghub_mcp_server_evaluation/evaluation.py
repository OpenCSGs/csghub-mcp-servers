import logging
from mcp.server.fastmcp import FastMCP
import json
from .api_client import (
    api_get_username_from_token,
)
from .api_client import evaluation, model, dataset, cluster, space_resources
from .utils import (
    get_csghub_api_endpoint, 
)

logger = logging.getLogger(__name__)

def register_evaluation_tools(mcp_instance: FastMCP):
    register_evaluation_list(mcp_instance=mcp_instance)
    register_evaluation_query(mcp_instance=mcp_instance)
    register_evaluation_create(mcp_instance=mcp_instance)
    register_evaluation_delete(mcp_instance=mcp_instance)

def register_evaluation_list(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="list_evaluation_services",
        title="List evaluation services for a user from CSGHub",
        description="Retrieve a list of evaluation services for a specific user from CSGHub. Parameters: `token` (str, required): User's API token. `username` (str, required): The user's namespace. You can control the pagination by specifying the number of items per page and the page number.",
        structured_output=True,
    )
    def list_evaluation(token: str, username: str, per: int = 10, page: int = 1) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        if not username:
            return "Error: The 'username' parameter is required."
        
        api_url = get_csghub_api_endpoint()
        
        try:
            evaluations = evaluation.list_evaluations(api_url, token, username, per, page)
            return json.dumps(evaluations)
        except Exception as e:
            logger.error(f"Error calling evaluation API: {e}")
            return f"Error: Failed to list evaluation services. {e}"

def register_evaluation_query(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="get_evaluation_by_id",
        title="Get evaluation details by numeric ID",
        description="Retrieve the evaluation details by a specific numeric ID from CSGHub with user access token. This is useful for checking the details of a evaluation that has been submitted to the CSGHub service.",
        structured_output=True,
    )
    def get_evaluation_by_id(token: str, id: int) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = evaluation.get_evaluation_details(api_url, token, id)
        return json.dumps({"data": json_data["data"]})

def register_evaluation_create(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="create_evaluation",
        title="Create a new evaluation task on CSGHub",
        description=(
            "Creates a new evaluation task on CSGHub. This is the final step of the evaluation creation process.\n"
            "It requires the following parameters:\n"
            "- `task_name`: A string for the name of the evaluation task.\n"
            "- `model_ids`: A list of model IDs to be evaluated. If you are unsure about the model IDs, you can use the `get_opencompass_models` tool to get a list of available models.\n"
            "- `runtime_framework_id`: An integer representing the ID of the runtime framework. You can get this ID by using the `get_model_runtime_framework` tool.\n"
            "- `datasets`: A list of dataset paths to be used for the evaluation. To get these paths, use the `get_opencompass_datasets` tool and extract the `path` field from each dataset object in the returned list.\n"
            "- `share_mode`: (Optional) A boolean to set whether the evaluation is public. Defaults to `True`. If `False`, `resource_id` is required.\n"
            "- `resource_id`: (Optional) An integer for the ID of the resource (e.g., hardware) to be used. This is only required when `share_mode` is `False`."
        ),
        structured_output=True,
    )
    def create_evaluation(token: str,
                          task_name: str,
                          model_ids: list[str],
                          runtime_framework_id: int,
                          datasets: list[str],
                          share_mode: bool = True,
                          resource_id: int = None,
                          ) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."

        if not share_mode and resource_id is None:
            return "Error: `resource_id` is required when `share_mode` is `False`. Please provide a `resource_id` and try again."
        
        api_url = get_csghub_api_endpoint()
        
        try:
            resp = evaluation.create_evaluation(api_url,
                                               token,
                                               task_name,
                                               model_ids,
                                               runtime_framework_id,
                                               datasets,
                                               share_mode,
                                               resource_id)
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling create evaluation API: {e}")
            return f"Error: Failed to create evaluation. {e}"
    
    @mcp_instance.tool(
        name="get_model_runtime_framework",
        title="Get model runtime framework by model ID and deploy type",
        description=(
            "Retrieves the available runtime frameworks for a specific model. This is a necessary step before creating an evaluation to get the `runtime_framework_id`.\n"
            "It requires the following parameters:\n"
            "- `model_id`: The ID of the model, for example: 'Qwen/Qwen2.5-0.5B-Instruct'. You can find model IDs using the `get_opencompass_models` tool.\n"
            "The `id` from the output of this tool is used as the `runtime_framework_id` parameter in the `create_evaluation` tool."
        ),
        structured_output=True,
    )
    def get_model_runtime_framework(token: str, model_id: str) -> str:
        api_url = get_csghub_api_endpoint()
        json_data = model.get_model_runtime_framework(api_url, token, model_id, deploy_type=4)
        return json.dumps({"data": json_data["data"]})

    @mcp_instance.tool(
        name="get_opencompass_datasets",
        title="Get OpenCompass datasets from CSGHub",
        description="Retrieves a list of datasets compatible with the OpenCompass framework. Each dataset in the returned list is an object, and you should use the value of the `path` field from these objects for the `datasets` parameter in the `create_evaluation` tool.",
        structured_output=True,
    )
    def get_opencompass_datasets(token: str) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        
        try:
            datasets = dataset.get_opencompass_datasets(api_url, token)
            return json.dumps(datasets)
        except Exception as e:
            logger.error(f"Error calling get opencompass datasets API: {e}")
            return f"Error: Failed to get opencompass datasets. {e}"

    @mcp_instance.tool(
        name="get_opencompass_models",
        title="Get OpenCompass models from CSGHub",
        description="Retrieves a list of models that are compatible with the OpenCompass evaluation framework. The model IDs returned by this tool can be used in the `model_ids` parameter of the `create_evaluation` and `get_model_runtime_framework` tools.",
        structured_output=True,
    )
    def get_opencompass_models(token: str) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        
        try:
            models = model.get_opencompass_models(api_url, token)
            return json.dumps(models)
        except Exception as e:
            logger.error(f"Error calling get opencompass models API: {e}")
            return f"Error: Failed to get opencompass models. {e}"

    @mcp_instance.tool(
        name="get_clusters",
        title="Get available clusters",
        description="Retrieve a list of available clusters. The `cluster_id` from the response can be used to get specific space resources.",
        structured_output=True,
    )
    def get_clusters(token: str) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        
        try:
            clusters = cluster.get_clusters(api_url, token)
            return json.dumps(clusters)
        except Exception as e:
            logger.error(f"Error calling get clusters API: {e}")
            return f"Error: Failed to get clusters. {e}"

    @mcp_instance.tool(
        name="get_space_resources",
        title="Get space resources for a cluster",
        description="Retrieve a list of available space resources for a given cluster. This is useful for finding the `resource_id` to use when creating an evaluation (`share_mode=False`). You need to provide a `cluster_id` from the `get_clusters` tool.",
        structured_output=True,
    )
    def get_space_resources(token: str, cluster_id: str) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        
        api_url = get_csghub_api_endpoint()
        
        try:
            resources = space_resources.get_space_resources(api_url, token, cluster_id, deploy_type=4)
            return json.dumps(resources)
        except Exception as e:
            logger.error(f"Error calling get space resources API: {e}")
            return f"Error: Failed to get space resources. {e}"

def register_evaluation_delete(mcp_instance: FastMCP):
    @mcp_instance.tool(
        name="delete_evaluation_by_id",
        title="Delete evaluation by numeric ID",
        description="Delete the evaluation by a specific numeric ID from CSGHub with user access token.",
        structured_output=True,
    )
    def delete_evaluation_by_id(token: str, id: int) -> str:
        if not token:
            return "Error: must input CSGHUB_ACCESS_TOKEN."
        api_url = get_csghub_api_endpoint()
        try:
            resp = evaluation.delete_evaluation(api_url, token, id)
            if not resp:
                return json.dumps({"message": "Evaluation deleted successfully"})
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling delete evaluation API: {e}")
            return f"Error: Failed to delete evaluation. {e}"
