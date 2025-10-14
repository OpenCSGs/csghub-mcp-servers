import argparse
from importlib.metadata import version, PackageNotFoundError

def get_version_from_package():
    try:
        return version("csghub-mcp-server")
    except PackageNotFoundError:
        return "unknown"

def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CSGHub MCP Server - A Model Context Protocol server for CSGHub",
        epilog="Example: python main.py --host 127.0.0.1 --port 8000 --log-level INFO"
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Server host address (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Server port number (default: 8000)'
    )

    parser.add_argument(
        '--protocol',
        type=str,
        choices=['stdio', 'sse', 'streamable-http'],
        default='streamable-http',
        help='protocol to use for communication (default: streamable-http)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'CSGHub MCP Server {get_version_from_package()}'
    )
    
    return parser