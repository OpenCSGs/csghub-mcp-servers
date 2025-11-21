import requests
import logging
from .constants import get_csghub_config, wrap_error_response

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
    if response.status_code != 200:
        logger.error(f"failed to list space resources on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data
    
    for res in res_list:
        res_data.append({
            "id": res["id"],
            "name": res["name"],
            "type": res["type"],
            "is_available": res["is_available"],
            "pay_mode": res["pay_mode"],
        })

    return res_data
