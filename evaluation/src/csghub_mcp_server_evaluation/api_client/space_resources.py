import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def get_space_resources(token: str, cluster_id: str, deploy_type: int) -> dict:
    """Get space resources.
    
    Args:
        token: User access token
        cluster_id: The ID of the cluster
        deploy_type: The type of deployment
        
    Returns:
        Space resources data
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/space_resources?cluster_id={cluster_id}&deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get space resources on {url}: {response.text}")

    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        if "is_available" in res and res["is_available"] == True:
            res_data.append({
                "id": res["id"],
                "type": res["type"],
                "name": res["name"]
            })

    return res_data
