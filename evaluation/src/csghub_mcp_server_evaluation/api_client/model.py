import requests
import logging

logger = logging.getLogger(__name__)

def get_opencompass_models(api_url: str, token: str) -> dict:
    """Get opencompass models.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        
    Returns:
        OpenCompass models data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models?tag_category=runtime_framework&tag_name=opencompass"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get opencompass models on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()

def get_model_runtime_framework(api_url: str, token: str, model_id: str, deploy_type: int) -> dict:
    """Get model runtime framework.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        model_id: The ID of the model
        deploy_type: The type of deployment
        
    Returns:
        Model runtime framework data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/{model_id}/runtime_framework_v2?deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model runtime framework on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()