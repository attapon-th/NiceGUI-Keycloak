#!/bin/bash


if [ ! -f .env ]; then
    echo ".env file does not exist"
    cat <<EOF > .env
PYTHONPATH=$(pwd)
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1


DEVMODE=1
DEBUG=True

PROJECT_PATH=$(pwd)
STORAGE_PATH=${PROJECT_PATH}/storage

APP_SECRET=$(openssl rand -hex 32)
APP_HOST=localhost
APP_PORT=8080
APP_BASEPATH=/app

OAUTH2_CLIENT_ID=__change_me__
OAUTH2_CLIENT_SECRET=__change_me__
OAUTH2_METADATA_URL=http://localhost:8080/auth/realms/master/.well-known/openid-configuration


NICEGUI_STORAGE_PATH=${STORAGE_PATH}/.nicegui
MATPLOTLIB=True
MARKDOWN_CONTENT_CACHE_SIZE=1000
RST_CONTENT_CACHE_SIZE=1000
NICEGUI_REDIS_URL=redis://localhost:6379/0
NICEGUI_REDIS_KEY_PREFIX=nicegui_oauth2
EOF
mkdir -p "${STORAGE_PATH}
fi