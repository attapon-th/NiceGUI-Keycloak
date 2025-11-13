# Nicegui OAuth2 With Keycloak

> TEMPLATE PROJECT - Replace this description with your project description.
>

This project is a web application built using the Nicegui framework that integrates OAuth2 authentication with Keycloak. It provides a simple interface for users to log in using their Keycloak credentials and access protected resources.

## File: .env
```dotenv
DEVMODE=0 # Set to 1 in development mode to enable debug features


PYTHONPATH=$(pwd)

PROJECT_PATH=$(pwd)
STORAGE_PATH=${PROJECT_PATH}/storage

APP_SECRET=this_is_a_secret_key_change_me
APP_HOST=localhost
APP_PORT=8080
APP_BASEPATH=/app

OAUTH2_CLIENT_ID=client-id
OAUTH2_CLIENT_SECRET=client-secret
OAUTH2_METADATA_URL=http://localhost:8081/realms/NiceguiOAuth2/.well-known/openid-configuration


NICEGUI_STORAGE_PATH=${STORAGE_PATH}/.nicegui
MATPLOTLIB=True
MARKDOWN_CONTENT_CACHE_SIZE=1000
RST_CONTENT_CACHE_SIZE=1000
NICEGUI_REDIS_URL=redis://localhost:6379/0
NICEGUI_REDIS_KEY_PREFIX=nicegui_oauth2
```