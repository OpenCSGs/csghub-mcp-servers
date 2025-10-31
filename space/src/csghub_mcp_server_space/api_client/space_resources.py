import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def get_space_resources(token: str, cluster_id: str, deploy_type: int) -> dict:
    """Get space resources.
    
    Args:
        token: User's token
        cluster_id: The ID of the cluster
        deploy_type: The type of deployment.
            0: space
            1: inference endpoint
            2: finetune
            3: serverless
            4: evaluation
            5: notebook
        
    Returns:
        Space resources data
    """
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/space_resources"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "cluster_id": cluster_id,
        "deploy_type": deploy_type
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()
