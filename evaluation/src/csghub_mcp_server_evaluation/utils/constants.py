import os

def get_csghub_api_endpoint():
     return os.getenv("CSGHUB_SERVER_ENDPOINT", "https://hub.opencsg.com")
