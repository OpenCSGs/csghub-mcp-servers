import requests
import logging

logger = logging.getLogger(__name__)

def api_get_dataset_detail(api_url: str, token: str, dataset_id: str) -> dict:
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/datasets/{dataset_id}"
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

if __name__ == "__main__":
    api_url = "https://hub.opencsg-stg.com"
    token = ""
    dataset_id = "wanghh2003/finetune-data"
    result = api_get_dataset_detail(api_url, token, dataset_id)
    print(result)
