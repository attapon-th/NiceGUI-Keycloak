# Nicegui OAuth2 With Keycloak

## File: .env
```dotenv
PYTHONPATH=$(pwd)
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1


DEVMODE=1
DEBUG=True

PROJECT_PATH=$(pwd)
STORAGE_PATH=${PROJECT_PATH}/storage

APP_SECRET=this_is_a_secret_key_change_me
APP_HOST=localhost
APP_PORT=8080
APP_BASEPATH=/app

OAUTH2_CLIENT_ID=admin-panal
OAUTH2_CLIENT_SECRET=admin-panal-secret
OAUTH2_METADATA_URL=http://localhost:8081/realms/NiceguiOAuth2/.well-known/openid-configuration


NICEGUI_STORAGE_PATH=${STORAGE_PATH}/.nicegui
MATPLOTLIB=True
MARKDOWN_CONTENT_CACHE_SIZE=1000
RST_CONTENT_CACHE_SIZE=1000
NICEGUI_REDIS_URL=redis://localhost:6379/0
NICEGUI_REDIS_KEY_PREFIX=nicegui_oauth2
```