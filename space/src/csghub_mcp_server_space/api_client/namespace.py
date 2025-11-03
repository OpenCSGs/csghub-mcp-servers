import requests
import logging
from .constants import get_csghub_config

logger = logging.getLogger(__name__)

def api_get_namespaces_by_token(token: str) -> str:
    config = get_csghub_config()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"{config.api_endpoint}/api/v1/organizations"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get namespaces on {url}: {response.text}")

    response.raise_for_status()
    json_data = response.json()
    print(json_data)
    namespaces = []
    if "data" in json_data:
        res_data = json_data["data"]
        if "data" in res_data:
            org_list = res_data["data"]
            if isinstance(org_list, list):
                for org in org_list:
                    namespaces.append(org["path"])
    return namespaces
