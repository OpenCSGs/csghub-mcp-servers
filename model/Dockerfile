FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

RUN pip install . --no-cache-dir

ENTRYPOINT ["csghub-mcp-server"]
