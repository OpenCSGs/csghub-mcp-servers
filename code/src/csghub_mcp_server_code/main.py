import time
import sys
import signal
import logging
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from .arguments import setup_argparse
from .code import register_code_tools

logger = logging.getLogger(__name__)

mcp = FastMCP("CSGHub-Code-MCP-Server", host="0.0.0.0", port=8000, log_level="INFO")

register_code_tools(mcp)

def signal_handler(sig, frame):
    logger.info("cleaning resource")
    time.sleep(1)
    sys.exit(0)

def pre_app(log_level: str = "INFO"):
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    change_global_log_format(log_level=log_level)

def change_global_log_format(log_level: str = "INFO"):
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    new_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    for handler in root_logger.handlers:
        handler.setFormatter(new_formatter)

def app(host: str = "0.0.0.0", port: int = 8000, protocol: str = 'streamable-http'):
    global mcp
    try:
        mcp.settings.host = host
        mcp.settings.port = port
        logger.info(f"Starting code MCP server on {host}:{port} with {protocol} protocol.")
        mcp.run(transport=protocol)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        logger.error(f"error happened: {e}")
        sys.exit(1)

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    pre_app(log_level=args.log_level)
    app(host=args.host, port=args.port, protocol=args.protocol)

if __name__ == "__main__":
    main()
