import requests
import logging
import random

logger = logging.getLogger(__name__)

def api_list_inferences(api_url: str, token: str, username: str, per: int = 10, page: int = 1) -> dict:
    """List inference services for a user.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        username: Username
        per: Items per page
        page: Page number
        
    Returns:
        Inference services data
    """
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
        "deploy_type": 1  # As for inference deploy
    }
    url = f"{api_url}/api/v1/user/{username}/run/model"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user inferences on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()

def api_get_inference_status(api_url: str, token: str, model_id: str, deploy_id: int) -> dict:
    """Get inference deployment status.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        model_id: Model repository path
        deploy_id: Deployment ID
        
    Returns:
        Inference status data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/run/{deploy_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get inferences status on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_inference_create(
    api_url: str,
    token: str,
    model_id: str,
    cluster_id: str,
    runtime_framework_id: int,
    resource_id: int,
    endpoint: str,
):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/run"
    random_num = f"{random.randint(0, 9999):04d}"
    json_data = {
        "cluster_id": cluster_id,
        "runtime_framework_id": runtime_framework_id,
        "resource_id": resource_id,
        "cost_per_hour": 0,
        "deploy_name": f"deploy_{random_num}",
        "env": "",
        "hardware": "",
        "max_replica": 1,
        "min_replica": 1,
        "revision": "main",
        "secure_level": 1,
        "entrypoint": endpoint,
    }
    response = requests.post(url, headers=headers, json=json_data)
    if response.status_code != 200:
        logger.error(f"failed to create model inference on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_inference_stop(api_url: str, token: str, model_id: str, deploy_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/run/{deploy_id}/stop"
    response = requests.put(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to stop model inference on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_inference_start(api_url: str, token: str, model_id: str, deploy_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/run/{deploy_id}/start"
    response = requests.put(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to start model inference on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def api_inference_delete(api_url: str, token: str, model_id: str, deploy_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/run/{deploy_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to delete model inference on {url}: {response.text}")

    response.raise_for_status()
    return response.json()


