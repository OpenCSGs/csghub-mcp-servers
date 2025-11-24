import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def api_get_available_resources(token: str, deploy_type: str) -> dict:
    clusters = get_clusters(token)
    config = get_csghub_config()
    ids = [id.strip() for id in config.cluster_ids.split(",") if id.strip()]
    res_data = []
    for cluster_id in ids:
        res = api_get_available_resources_by_cluster(cluster_id, deploy_type, clusters)
        if res and isinstance(res, list):
            res_data.append(res)

    return res_data

def get_clusters(token: str) -> dict:
    config = get_csghub_config()
    url = f"{config.api_endpoint}/api/v1/cluster"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.error(f"failed to list clusters on {url}: {response.text}")
        return wrap_error_response(response)

    response.raise_for_status()
    json_data = response.json()

    res_dict = {}
    res_list = json_data["data"] if json_data and "data" in json_data else []
    
    if not isinstance(res_list, list):
        return res_dict
    
    for res in res_list:
        cluster_id = res["cluster_id"]
        region = res["region"]
        res_dict[cluster_id] = region

    return res_dict


def api_get_available_resources_by_cluster(cluster_id: str, deploy_type: str, clusters: dict) -> list:
    config = get_csghub_config()
    headers = {"Content-Type": "application/json"}
    url = f"{config.api_endpoint}/api/v1/space_resources?cluster_id={cluster_id}&deploy_type={deploy_type}"
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
        skip = True
        if "is_available" in res and res["is_available"] == True:
            skip = False
        
        if skip:
            continue

        price = "free"
        priceVal = res["price"] if "price" in res else 0.0
        priceUnitVal = res["price_unit"] if "price_unit" in res else 0.0
        priceUnitTypeVal = res["price_unit_type"] if "price_unit_type" in res else "minute"
        if priceVal > 0 and priceUnitVal > 0:
            if priceUnitTypeVal.lower() == "minute":
                price = f"￥ {priceVal / 100} / {priceUnitVal/60} hour"
            else:
                price = f"￥ {priceVal / 100} / {priceUnitVal} {priceUnitTypeVal}"

        cluster_name = clusters[cluster_id] if clusters[cluster_id] else "unknown"
        res_data.append({
            "cluster_name": cluster_name,
            "cluster_id": cluster_id,
            "id": res["id"],
            "type": res["type"],
            "name": res["name"],
            "price": f"{price}"
        })

    return res_data
