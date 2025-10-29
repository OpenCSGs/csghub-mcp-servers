import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def get_clusters(token: str) -> dict:
    """Get cluster information.
    
    Args:
        api_url: CSGHub API base URL
        token: User's token
        
    Returns:
        Cluster data
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/cluster"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
