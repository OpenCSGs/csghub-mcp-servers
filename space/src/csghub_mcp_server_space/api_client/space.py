import requests
import logging

logger = logging.getLogger(__name__)

def api_get_top_download_spaces(api_url: str, num: int) -> dict:
    """Get top downloaded spaces.
    
    Args:
        api_url: CSGHub API base URL
        num: Number of spaces to retrieve
        
    Returns:
        Top spaces data
    """
    headers = {"Content-Type": "application/json"}
    params = {
        "page": 1,
        "per": num,
        "search": "",
        "sort": "most_download"
    }
    url = f"{api_url}/api/v1/spaces"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"failed to get spaces on {url}: {response.text}")
        
    response.raise_for_status()
    return response.json()