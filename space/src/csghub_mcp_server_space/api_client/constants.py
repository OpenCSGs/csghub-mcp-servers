import os
from dataclasses import dataclass

@dataclass
class CSGHubConfig:    
    api_endpoint: str = None
    web_endpoint: str = None
    cluster_ids: str = None
    
    def __post_init__(self):
        self.api_endpoint = self.api_endpoint or os.getenv("CSGHUB_SERVER_ENDPOINT", "https://hub.opencsg.com")
        self.web_endpoint = self.web_endpoint or os.getenv("CSGHUB_WEB_ENDPOINT", "https://opencsg.com")
        self.cluster_ids = self.cluster_ids or os.getenv("CLUSTER_ID", "ab45d3ba-a2ff-466e-887a-b2e5c0c070c5")

def get_csghub_config() -> CSGHubConfig:
    return CSGHubConfig()

def wrap_error_response(response) -> dict:
    return {
        "error_code": response.status_code,
        "error_message": response.text,
    }

