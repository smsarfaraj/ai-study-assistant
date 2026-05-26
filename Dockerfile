FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies (no dev group)
RUN uv sync --no-dev

# Copy source
COPY src/ ./src/

# Create data directory
RUN mkdir -p data/chroma

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.api.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
