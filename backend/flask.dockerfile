FROM ghcr.io/astral-sh/uv:0.6.9-python3.13-bookworm-slim

# Set environment variables to use the project's virtual environment
ENV UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    UV_PYTHON=python3.13

# Create app directory and set working directory
WORKDIR /app

# Install dependencies from pyproject.toml and uv.lock
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

COPY . .

# Install the project in development mode
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 4000
CMD ["uv", "run", "flask", "run", "--host=0.0.0.0", "--port=4000"]