import logging
import json
from mcp.server.fastmcp import FastMCP
from .api_client import space, user
from .utils import constants

logger = logging.getLogger(__name__)

def register_run_tool(mcp_instance: FastMCP):

    @mcp_instance.tool(
        name="run_space",
        title="Run a CSGHub space",
        description="Starts a CSGHub space. Parameters: `token` (str, required): User's API token. `space_name` (str, required): Name of the space to run.",
        structured_output=True,
    )
    def run_space(
        token: str,
        space_name: str,
    ) -> str:
        """
        Run a CSGHub space.

        Args:
            token: User's API token.
            space_name: Name of the space.
        """
        api_url = constants.get_csghub_api_endpoint()
        api_key = constants.get_csghub_api_key()

        if not token:
            return "Error: The 'token' parameter is required."
        if not space_name:
            return "Error: The 'space_name' parameter is required."

        try:
            username = user.get_username_from_token(api_url, api_key, token)
        except Exception as e:
            logger.error(f"Error calling user token API: {e}")
            return f"Error: Failed to get username. {e}"

        try:
            resp = space.run_space(
                api_url=api_url,
                token=token,
                namespace=username,
                space_name=space_name,
            )
            return json.dumps(resp)
        except Exception as e:
            logger.error(f"Error calling run space API: {e}")
            return f"Error: Failed to run space. {e}"
