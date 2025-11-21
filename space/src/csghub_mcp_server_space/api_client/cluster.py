import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def get_clusters(token: str) -> dict:
    """Get cluster information.
    
    Args:
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
    if response.status_code != 200:
        logger.error(f"failed to list clusters on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data
    
    for res in res_list:
        res_data.append({
            "cluster_id": res["cluster_id"],
            "status": res["status"],
            "region": res["region"],
        })

    return res_data
