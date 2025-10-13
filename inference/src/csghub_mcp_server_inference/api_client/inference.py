import requests
import logging

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
