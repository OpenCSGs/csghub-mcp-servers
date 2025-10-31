import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def get_opencompass_models(token: str) -> dict:
    """Get opencompass models.
    
    Args:
        token: User access token
        
    Returns:
        OpenCompass models data
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models?tag_category=runtime_framework&tag_name=opencompass"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get opencompass models on {url}: {response.text}")
    
    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "model_id": res["path"]
        })

    return res_data

def get_model_runtime_framework(token: str, model_id: str, deploy_type: int) -> dict:
    """Get model runtime framework.
    
    Args:
        token: User access token
        model_id: The ID of the model
        deploy_type: The type of deployment
        
    Returns:
        Model runtime framework data
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/runtime_framework_v2?deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model runtime framework on {url}: {response.text}")
    
    json_data = response.json()
    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []

    for res in res_list:
        if "versions" in res:
            ver_list = res["versions"]
            for ver in ver_list:
                if ver["enabled"] == 1:
                    res_data.append({
                        "id": ver["id"],
                        "frame_name": ver["frame_name"],
                        "compute_type": ver["compute_type"],
                    })

    return res_data