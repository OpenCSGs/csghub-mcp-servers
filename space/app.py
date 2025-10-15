import logging
from src.csghub_mcp_server_space.main import app
from src.csghub_mcp_server_space.arguments import setup_argparse
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = setup_argparse()
    args = parser.parse_args()
    if args.env_file:
        logger.info(f"Load .env from: {args.env_file}")
        load_dotenv(dotenv_path=args.env_file)
    else:
        load_dotenv()
    # streamable-http
    # app(host='0.0.0.0', port=8000, protocol='streamable-http')
    # sse
    # app(host='0.0.0.0', port=8000, protocol='stdio')
    app(host='0.0.0.0', port=8000, protocol=args.protocol)
