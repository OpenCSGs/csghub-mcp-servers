import requests
import logging

logger = logging.getLogger(__name__)

def api_top_download_models(api_url: str, num: int) -> dict:
    """Get top downloaded models.
    
    Args:
        api_url: CSGHub API base URL
        num: Number of models to retrieve
        
    Returns:
        Top models data
    """
    headers = {"Content-Type": "application/json"}
    params = {
        "page": 1,
        "per": num,
        "search": "",
        "sort": "most_download"
    }
    url = f"{api_url}/api/v1/models"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get top {num} downloaded models on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()