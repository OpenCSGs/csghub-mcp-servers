import requests
import logging

logger = logging.getLogger(__name__)

def api_get_available_runtime_frameworks(api_url: str, model_id: str, deploy_type: str) -> dict:
    headers = {"Content-Type": "application/json"}
    url = f"{api_url}/api/v1/models/{model_id}/runtime_framework_v2?deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get avai resources on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()

def api_get_available_runtime_frameworks_by_deploy_type(api_url: str, token: str, deploy_type: str) -> dict:
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/runtime_framework?deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get avai resources on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()
