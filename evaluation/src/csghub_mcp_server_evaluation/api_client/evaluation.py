import requests
import logging
from .constants import get_csghub_config
from .user import api_get_username_from_token

logger = logging.getLogger(__name__)

def list_evaluations(token: str, per: int = 10, page: int = 1) -> dict:
    """List evaluation services for a user.
    
    Args:
        token: User access token
        username: Username
        per: Items per page
        page: Page number
        
    Returns:
        Evaluation services data
    """
    config = get_csghub_config()

    try:
        username = api_get_username_from_token(token)
    except Exception as e:
        logger.error(f"Error calling user token API: {e}")
        return f"Error: Failed to get username. {e}"

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{config.api_endpoint}/api/v1/user/{username}/evaluations"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user evaluations on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "id": res["id"],
            "task_id": res["task_id"],
            "task_name": res["task_name"],
            "dataset_ids": res["datasets"],
            "models": res["repo_ids"],
            "status": res["status"],
        })

    return res_data

def get_evaluation_details(token: str, id: int) -> dict:
    """Get evaluaton details.
    
    Args:
        token: User access token
        id: Evaluation ID
        
    Returns:
        evaluation data
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/evaluations/{id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get eval details on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()

    json_data = response.json()

    eval_data = {}
    res_data = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_data, object):
        return res_data
    print(res_data)
    eval_data = {
        "id": res_data["id"],
        "task_id": res_data["task_id"],
        "task_name": res_data["task_name"],
        "model_ids": res_data["repo_ids"],
        "status": res_data["status"],
        "result_url": res_data["result_url"],
        "download_url": res_data["download_url"],
    }

    return eval_data

def create_evaluation(token: str,
                    task_name: str,
                    model_ids: list[str],
                    runtime_framework_id: int,
                    datasets: list[str],
                    share_mode: bool = True,
                    resource_id: int = None) -> dict:
    """Create a new evaluation task.
    
    Args:
        token: User access token
        task_name: Name of the evaluation task
        model_ids: List of model IDs to be evaluated
        runtime_framework_id: ID of the runtime framework
        datasets: List of datasets to be used for evaluation
        share_mode: Whether the evaluation is shared
        resource_id: ID of the resource to be used
        
    Returns:
        Response from the API
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/evaluations"
    payload = {
        "task_name": task_name,
        "model_ids": model_ids,
        "runtime_framework_id": runtime_framework_id,
        "share_mode": share_mode,
        "datasets": datasets,
    }
    if resource_id is not None:
        payload["resource_id"] = resource_id
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        logger.error(f"failed to create evaluation on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }
    
    response.raise_for_status()
    json_data = response.json()

    eval_data = {}
    res_data = json_data["data"] if json_data and "data" in json_data else []

    if not isinstance(res_data, object):
        return eval_data

    eval_data = {
        "id": res_data["id"],
        "task_id": res_data["task_id"],
        "task_name": res_data["task_name"],
        "model_ids": res_data["repo_ids"],
    }

    return eval_data 

def delete_evaluation(token: str, evaluation_id: int) -> dict:
    """Delete an evaluation task.

    Args:
        token: User access token
        evaluation_id: ID of the evaluation task to be deleted

    Returns:
        Response from the API
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/evaluations/{evaluation_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code not in [200, 204]:
        logger.error(f"failed to delete evaluation on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }

    response.raise_for_status()
    if response.status_code == 204:
        return {}
    return response.json()
