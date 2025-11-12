FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --locked

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv ./.venv
COPY src/ ./src/
EXPOSE 8000
CMD [ "/app/.venv/bin/uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000" ]