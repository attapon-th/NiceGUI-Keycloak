FROM python:3.12-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app

COPY uv.lock pyproject.toml /app/
COPY app /app/app
copy static /app/static

# Core Configuration
ENV UV_PROJECT_ENVIRONMENT=/venv \
    UV_NO_MANAGED_PYTHON=1 \
    UV_PYTHON_DOWNLOADS=never \
    VIRTUAL_ENV=/venv

# Performance Optimizations
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_CACHE_DIR=/app/.cache/uv

# Security and Reproducibility
ENV UV_FROZEN=1 \
    UV_REQUIRE_HASHES=1 \
    UV_VERIFY_HASHES=1


# Create the virtual environment
RUN uv venv $VIRTUAL_ENV

# Install dependencies with mount caching
ARG BUILD_GROUPS=""
RUN --mount=type=cache,target=/app/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --no-install-project --no-editable $BUILD_GROUPS


### FINAL IMAGE ###
FROM python:3.13-slim-bookworm

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV TZ=Asia/Bangkok \
    PYTHONPATH=/app \
    PATH="/venv/bin:$PATH" \
    PORT=${PORT} \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/venv 

# Application Configuration
ENV PROJECT_PATH=/app \
    STORAGE_PATH=/app/storage \
    NICEGUI_STORAGE_PATH=/app/storage/.nicegui \
    APP_HOST=0.0.0.0 \
    APP_PORT=8080 \
    APP_BASEPATH=/app \
    MATPLOTLIB=True \
    MARKDOWN_CONTENT_CACHE_SIZE=1000 \
    RST_CONTENT_CACHE_SIZE=1000 \
    NICEGUI_REDIS_KEY_PREFIX=nicegui_oauth2


# Copy selectively from builder to optimize final image.
# --link enables better layer caching when base image changes
COPY --link --from=builder /venv /venv
COPY --link --from=builder /app/app /app/app
COPY --link --from=builder /app/static /app/static