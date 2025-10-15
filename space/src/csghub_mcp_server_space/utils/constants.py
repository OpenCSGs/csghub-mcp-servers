import os

def get_csghub_api_endpoint():
     return os.getenv("CSGHUB_SERVER_ENDPOINT", "https://hub.opencsg.com")

def get_csghub_api_key():
     return os.getenv("CSGHUB_SERVER_API_TOKEN", "")
