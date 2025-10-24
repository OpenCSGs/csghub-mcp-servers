import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_get_available_resources(cluster_id: str, deploy_type: str) -> dict:
    config = get_csghub_config()

    headers = {"Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/space_resources?cluster_id={cluster_id}&deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get avai resources on {url}: {response.text}")
    
    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    for res in res_list:
        if "type" in res and res["type"].lower() == "gpu" and "is_available" in res and res["is_available"] == True:
            res_data.append({
                "id": res["id"],
                "type": res["type"],
                "name": res["name"]
            })

    return res_data

if __name__ == "__main__":
    cluster_id = "1b25151b-690b-42a4-b18b-aa1c86bd2696"
    deploy_type = "6"
    result = api_get_available_resources(cluster_id, deploy_type)
    print(result)

