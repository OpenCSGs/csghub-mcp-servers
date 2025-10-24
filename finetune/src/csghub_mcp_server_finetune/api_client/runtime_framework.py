import requests
import logging

logger = logging.getLogger(__name__)

def api_get_available_runtime_frameworks(api_url: str, model_id: str, deploy_type: str) -> dict:
    headers = {"Content-Type": "application/json"}
    url = f"{api_url}/api/v1/models/{model_id}/runtime_framework_v2?deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get avai resources on {url}: {response.text}")
    
    json_data = response.json()
    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []

    for res in res_list:
        if "compute_types" in res and "gpu" in res["compute_types"] and "versions" in res:
            ver_list = res["versions"]
            for ver in ver_list:
                if ver["enabled"] == 1:
                    res_data.append({
                        "id": ver["id"],
                        "frame_name": ver["frame_name"],
                        "compute_type": ver["compute_type"],
                    })

    return res_data

def api_get_available_runtime_frameworks_by_deploy_type(api_url: str, token: str, deploy_type: str) -> dict:
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    url = f"{api_url}/api/v1/models/runtime_framework?deploy_type={deploy_type}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to get avai resources on {url}: {response.text}")
    
    response.raise_for_status()
    json_data = response.json()

    res_data = []
    res_list = json_data["data"] if json_data and "data" in json_data else []
    for res in res_list:
        if "compute_type" in res and res["compute_type"].lower() == "gpu" and "enabled" in res and res["enabled"] == 1:
            res_data.append({
                "id": res["id"],
                "frame_name": res["frame_name"],
            })

    return res_data

if __name__ == "__main__":
    api_url = "https://hub.opencsg-stg.com"
    token = ""
    deploy_type = "6"
    result = api_get_available_runtime_frameworks_by_deploy_type(api_url, token, deploy_type)
    # result = api_get_available_runtime_frameworks(api_url, "Qwen/Qwen3-0.6B", "2")
    print(result)
