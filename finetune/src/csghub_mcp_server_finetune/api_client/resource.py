import requests
import logging

logger = logging.getLogger(__name__)

def api_get_available_resources(api_url: str, cluster_id: str, deploy_type: str) -> dict:
    headers = {"Content-Type": "application/json"}
    url = f"{api_url}/api/v1/space_resources?cluster_id={cluster_id}&deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get avai resources on {url}: {response.text}")
    
    response.raise_for_status()
    return response.json()
