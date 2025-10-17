import requests
import logging

logger = logging.getLogger(__name__)

def api_get_model_detail(api_url: str, model_id: str) -> dict:
    """Get top downloaded models.
    
    Args:
        api_url: CSGHub API base URL
        num: Number of models to retrieve
        
    Returns:
        Top models data
    """
    headers = {"Content-Type": "application/json"}
    url = f"{api_url}/api/v1/models/{model_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model detail on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()

def api_get_model_quantizations_list(api_url: str, model_id: str) -> dict:
    headers = {"Content-Type": "application/json"}
    url = f"{api_url}/api/v1/models/{model_id}/quantizations"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model quantizations on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()
