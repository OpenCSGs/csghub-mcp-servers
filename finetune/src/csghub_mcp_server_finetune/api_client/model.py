import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def api_get_model_detail(token: str, model_id: str) -> dict:
    config = get_csghub_config()

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
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

if __name__ == "__main__":
    token = ""
    model_id = "wanghh2003/Qwen3-0.6B"
    result = api_get_model_detail(token, model_id)
    print(result)
