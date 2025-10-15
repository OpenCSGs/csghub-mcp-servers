import requests
import logging

logger = logging.getLogger(__name__)

def get_space_resources(api_url: str, token: str, cluster_id: str, deploy_type: int) -> dict:
    """Get space resources.
    
    Args:
        api_url: CSGHub API base URL
        token: User access token
        cluster_id: The ID of the cluster
        deploy_type: The type of deployment
        
    Returns:
        Space resources data
    """
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/space_resources?cluster_id={cluster_id}&deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get space resources on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()
