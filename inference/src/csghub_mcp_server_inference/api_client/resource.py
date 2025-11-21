import requests
import logging
from .constants import get_csghub_config, wrap_error_response

logger = logging.getLogger(__name__)

def api_get_available_resources(cluster_id: str, deploy_type: str) -> dict:
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

        res_data.append({
            "id": res["id"],
            "type": res["type"],
            "name": res["name"],
            "price": f"{price}"
        })

    return res_data
