import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def api_get_available_runtime_frameworks(model_id: str, deploy_type: str) -> dict:
    config = get_csghub_config()
    headers = {"Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/models/{model_id}/runtime_framework_v2?deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get avai resources on {url}: {response.text}")
        return wrap_error_response(response)
    
    response.raise_for_status()

    json_data = response.json()
    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []

    if not isinstance(res_list, list):
        return res_data

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
