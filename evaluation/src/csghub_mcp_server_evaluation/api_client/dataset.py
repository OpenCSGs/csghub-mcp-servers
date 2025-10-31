import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def get_opencompass_datasets(token: str) -> dict:
    """Get opencompass datasets.
    
    Args:
        token: User access token
        
    Returns:
        OpenCompass datasets data
    """
    config = get_csghub_config()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/datasets?tag_category=runtime_framework&tag_name=opencompass"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get opencompass datasets on {url}: {response.text}")
    
    response.raise_for_status()

    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []

    if not isinstance(res_list, list):
        return res_data

    for res in res_list:
        res_data.append({
            "dataset_id": res["path"]
        })

    return res_data
