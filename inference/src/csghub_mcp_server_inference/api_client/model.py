import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_get_model_detail(model_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model detail on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }
    
    response.raise_for_status()
    json_data = response.json()
    res_data = {}
    if json_data and "data" in json_data:
        res_data = {
            "model_id": json_data["data"]["path"]
        }

    return res_data

def api_get_model_quantizations_list(model_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/quantizations"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model quantizations on {url}: {response.text}")
        return {
            "error_code": response.status_code,
            "error_message": response.text,
        }
    
    response.raise_for_status()
    return response.json()
