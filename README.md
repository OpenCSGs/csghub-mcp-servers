# CSGHub MCP Servers

## Overview

CSGHub MCP (Model Control Panel) Servers is a specialized service component designed to provide model control tools for the CSGHub server ecosystem. This project serves as a bridge between CSGHub's core functionality and advanced management capabilities, enabling efficient control and operation of AI models within the CSGHub platform.

## Features

- **Model Control Interface**: Provides a unified interface for managing AI models in CSGHub
- **Tool Integration**: Seamlessly integrates with CSGHub's existing toolchain
- **MCP API Support**: Offers MCP tools APIs for programmatic access to model control functions
- **Extensible Architecture**: Designed to be easily extended with new control capabilities
- **Lightweight Implementation**: Minimal dependencies for easy deployment and maintenance

## Requirements

- Python 3.10 or higher
- CSGHub Server environment

## Installation

### Create a Virtual Environment

```bash
uv venv --python 3.10

source .venv/bin/activate
```

### From Source

Clone the repository and install the package:

```bash
git clone https://jihulab.com/opencsg/csghub-mcp-servers.git
cd csghub-mcp-server/model

uv pip install .
```

### Run the Server

```bash
# Run by command
csghub-mcp-server

# Run by uv
uv run src/csghub_mcp_server/main.py
```

### Add dependencies

```bash
uv add requests mcp

uv pip install mcp
```