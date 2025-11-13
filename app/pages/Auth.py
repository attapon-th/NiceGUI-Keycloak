from functools import cache

import requests
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request
from fastapi.datastructures import URL
from nicegui import app, ui
from starlette.responses import RedirectResponse
from typing import Any, Optional
from app.pkgs.config import Config, get_config
from datetime import datetime
from loguru import logger as log

conf: Config = get_config()
log.level("DEBUG")

oauth = OAuth()
oauth.register(
    name="keycloak",
    server_metadata_url=conf.OAUTH2_METADATA_URL,
    client_id=conf.OAUTH2_CLIENT_ID,
    client_secret=conf.OAUTH2_CLIENT_SECRET,
    client_kwargs={"scope": "openid email profile"},
)


authorize_redirect = oauth.keycloak.authorize_redirect  # type: ignore


@cache
def get_metadata_keycloak() -> dict:
    response = requests.get(conf.OAUTH2_METADATA_URL)
    if response.status_code == 200:
        return response.json()
    else:
        log.error(f"Failed to get metadata: {response.status_code}")
        raise Exception(f"Failed to get metadata: {response.status_code}")


async def login(request: Request) -> Optional[RedirectResponse]:
    user_data = app.storage.user.get("user_data", {})
    if user_data:
        return RedirectResponse("/")
    else:
        url: URL = request.url_for("auth_route")
        return await authorize_redirect(request, redirect_uri=url)  # type: ignore


async def keycloak_oauth(request: Request) -> RedirectResponse:
    u = request.url_for("index_route")
    try:
        user_data = await oauth.keycloak.authorize_access_token(request)  # type: ignore
    except OAuthError as e:
        log.error(f"OAuth error: {e}", exc_info=True)
        return RedirectResponse(u)  # or return an error page/message
    app.storage.user["user_data"] = user_data
    return RedirectResponse(u)  # Redirect to the home page after successful login


async def logout(request: Request) -> RedirectResponse:
    try:
        if "user_data" in app.storage.user:
            del app.storage.user["user_data"]
        metadata = get_metadata_keycloak()
        logout_url = metadata.get("end_session_endpoint", "")
        # Ensure the home page is accessible after logout
        u: URL = URL(logout_url)
        u = u.replace_query_params(
            **{
                "client_id": conf.OAUTH2_CLIENT_ID,
                "post_logout_redirect_uri": request.url_for("index_route"),
            }
        )
        return RedirectResponse(str(u))
    except Exception as e:
        log.error(f"Logout error: {e}", exc_info=True)
        u = request.url_for("index_route")
    return RedirectResponse("/")

async def refresh_token(request: Request) -> bool:
    user_data = app.storage.user.get("user_data", {})
    # return True
    refresh_token = user_data.get("refresh_token", "")
    if refresh_token:
        try:
            new_tokens = await oauth.keycloak.fetch_access_token()  # type: ignore
            user_data.update(new_tokens)
            app.storage.user["user_data"] = user_data
            # ex = datetime.fromtimestamp(new_tokens.get("expires_at", 0))
            # ui.notify(f"Token refreshed successfully, expires at {ex.strftime('%Y-%m-%d %H:%M:%S')}", color="positive")

            return True
        except Exception as e:
            log.error(f"Token refresh failed: {e}", exc_info=True)
            del app.storage.user["user_data"]
            ui.navigate.to("/login")
    return False


async def get_userdata(request: Request) -> Optional[dict[str, Any]]:
    try:
        user_data = app.storage.user.get("user_data", {})
        if user_data:
            expires_at = user_data.get("expires_at", 0)
            current_time = datetime.now().timestamp()

            if current_time < expires_at - (2 * 60): # 2 minutes buffer
                return user_data  # Token expired, return user data to trigger refresh
            elif await refresh_token(request):
                user_data = app.storage.user.get("user_data", {})
                return user_data
    except Exception as e:
        # ui.notify(f"Error getting user data: {e}", color="negative")
        log.error(f"Error getting user data: {e}", exc_info=True)

    return None
