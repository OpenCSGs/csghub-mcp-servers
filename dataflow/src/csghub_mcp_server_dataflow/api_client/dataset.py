import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_get_dataset_detail(token: str, dataset_id: str) -> dict:
    config = get_csghub_config()

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    url = f"{config.api_endpoint}/api/v1/datasets/{dataset_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get dataset detail on {url}: {response.text}")
    
    response.raise_for_status()
    json_data = response.json()
    res_data = {}
    if json_data and "data" in json_data:
        res_data = {
            "dataset_id": json_data["data"]["path"]
        }

    return res_data

