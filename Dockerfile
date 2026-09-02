FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN apt update -y && apt install pkg-config default-libmysqlclient-dev build-essential -y

COPY . /app

WORKDIR /app/backend
RUN uv sync --frozen

CMD ["/app/backend/.venv/bin/fastapi", "run", "src/main.py", "--port", "8000", "--host", "0.0.0.0"]
