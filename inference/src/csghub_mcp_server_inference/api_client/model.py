import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def api_get_model_detail(model_id: str) -> dict:
    config = get_csghub_config()
    headers = {"Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get model detail on {url}: {response.text}")
        return wrap_error_response(response)
    
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
        return wrap_error_response(response)
    
    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    
    if not isinstance(res_list, list):
        return res_data
    
    for item in res_list:
        res_data.append(item["name"])

    return res_data
