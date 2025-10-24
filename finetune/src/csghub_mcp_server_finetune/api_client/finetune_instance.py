import requests
import logging
import random

logger = logging.getLogger(__name__)

def api_list_finetunes(api_url: str, token: str, username: str, per: int = 10, page: int = 1) -> dict:
    """List finetune services for a user.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        username: Username
        per: Items per page
        page: Page number
        
    Returns:
        Finetune services data
    """
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{api_url}/api/v1/user/{username}/finetune/instances"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user finetunes on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_get_finetune_status(api_url: str, token: str, model_id: str, deploy_id: int) -> dict:
    """Get finetune deployment status.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        model_id: Model repository path
        deploy_id: Deployment ID
        
    Returns:
        finetune status data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/run/{deploy_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get inferences status on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_finetune_create(
    api_url: str,
    token: str,
    model_id: str,
    cluster_id: str,
    runtime_framework_id: int,
    resource_id: int,
):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/finetune"
    random_num = f"{random.randint(0, 9999):04d}"
    json_data = {
        "deploy_name": f"finetune_{random_num}",
        "cluster_id": cluster_id,
        "resource_id": resource_id,
        "runtime_framework_id": runtime_framework_id,
        "revision": "main",
        "order_detail_id": 0,
        "engine_args": "",
    }
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code != 200:
        logger.error(f"failed to create finetune on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_finetune_stop(api_url: str, token: str, model_id: str, deploy_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/finetune/{deploy_id}/stop"
    response = requests.put(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to stop model finetune on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_finetune_start(api_url: str, token: str, model_id: str, deploy_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/finetune/{deploy_id}/start"
    response = requests.put(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to start model finetune on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_finetune_delete(api_url: str, token: str, model_id: str, deploy_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/finetune/{deploy_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete model finetune on {url}: {response.text}")

    response.raise_for_status()
    return response.json()
