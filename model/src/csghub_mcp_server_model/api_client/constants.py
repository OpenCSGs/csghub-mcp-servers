import os
from dataclasses import dataclass

@dataclass
class CSGHubConfig:    
    api_endpoint: str = None
    web_endpoint: str = None
    api_key: str = None
    
    def __post_init__(self):
        self.api_endpoint = self.api_endpoint or os.getenv("CSGHUB_SERVER_ENDPOINT", "https://hub.opencsg.com")
        self.web_endpoint = self.web_endpoint or os.getenv("CSGHUB_WEB_ENDPOINT", "https://opencsg.com")
        self.api_key = self.api_key or os.getenv("CSGHUB_SERVER_API_TOKEN", "")

def get_csghub_config() -> CSGHubConfig:
    return CSGHubConfig()

