import requests
import logging

logger = logging.getLogger(__name__)

def get_opencompass_datasets(api_url: str, token: str) -> dict:
    """Get opencompass datasets.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        
    Returns:
        OpenCompass datasets data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/datasets?tag_category=runtime_framework&tag_name=opencompass"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get opencompass datasets on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()
