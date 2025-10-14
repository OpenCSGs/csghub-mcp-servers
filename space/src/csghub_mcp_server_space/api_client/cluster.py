import requests
import logging

logger = logging.getLogger(__name__)

def get_clusters(api_url: str, token: str) -> dict:
    """Get cluster information.
    
    Args:
        api_url: CSGHub API base URL
        token: User's token
        
    Returns:
        Cluster data
    """
    url = f"{api_url}/api/v1/cluster"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
