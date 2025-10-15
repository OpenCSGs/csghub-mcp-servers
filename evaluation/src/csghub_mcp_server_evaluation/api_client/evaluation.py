import requests
import logging

logger = logging.getLogger(__name__)

def list_evaluations(api_url: str, token: str, username: str, per: int = 10, page: int = 1) -> dict:
    """List evaluation services for a user.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        username: Username
        per: Items per page
        page: Page number
        
    Returns:
        Evaluation services data
    """
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "per": per,
        "page": page,
    }
    url = f"{api_url}/api/v1/user/{username}/evaluations"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to list user evaluations on {url}: {response.text}")

    response.raise_for_status()
    return response.json()

def get_evaluation_details(api_url: str, token: str, id: int) -> dict:
    """Get evaluaton details.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        id: Evaluation ID
        
    Returns:
        evaluation data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/evaluations/{id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def create_evaluation(api_url: str,
                          token: str,
                          task_name: str,
                          model_ids: list[str],
                          runtime_framework_id: int,
                          datasets: list[str],
                          share_mode: bool = True,
                          resource_id: int = None) -> dict:
    """Create a new evaluation task.
    
    Args:
        api_url: CSGHub API base URL
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
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{api_url}/api/v1/evaluations"
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
    
    response.raise_for_status()
    return response.json()