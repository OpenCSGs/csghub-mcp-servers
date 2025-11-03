# CSGHub Code MCP Tools

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
git clone https://github.com/OpenCSGs/csghub-mcp-servers.git
cd csghub-mcp-servers/dataset

uv pip install .
```

### Run the Server

```bash
# Run by command
csghub-mcp-server-dataset

# Run locally
python app.py
```

### Add dependencies

```bash
uv add requests mcp

uv pip install mcp
```

