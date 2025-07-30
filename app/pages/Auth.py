from functools import cache

import requests
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request
from fastapi.datastructures import URL
from nicegui import app, ui
from starlette.responses import RedirectResponse

from app.pkgs.config import Config, get_config

conf: Config = get_config()


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
        raise Exception(f"Failed to get metadata: {response.status_code}")


async def check_access_token() -> bool:
    """
    Check if the current access token is valid.
    """
    if "user_data" not in app.storage.user or not app.storage.user.get("user_data"):
        return False
    
    user_data = app.storage.user["user_data"]
    access_token = user_data.get("access_token")
    
    if not access_token:
        # Try to refresh the token if refresh_token is available
        refresh_token = user_data.get("refresh_token")
        if refresh_token:
            
            try:
                metadata = get_metadata_keycloak()
                token_endpoint = metadata.get("token_endpoint")
                
                if token_endpoint:
                    refresh_data = {
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token,
                        "client_id": conf.OAUTH2_CLIENT_ID,
                        "client_secret": conf.OAUTH2_CLIENT_SECRET,
                    }
                    
                    response = requests.post(token_endpoint, data=refresh_data)
                    
                    if response.status_code == 200:
                        new_tokens = response.json()
                        # Update user data with new tokens
                        user_data.update(new_tokens)
                        app.storage.user["user_data"] = user_data
                        return True
            except Exception as e:
                print(f"Token refresh failed: {e}")
        return False
    
    # Get userinfo endpoint from metadata
    metadata =  get_metadata_keycloak()
    userinfo_endpoint = metadata.get("userinfo_endpoint")
    
    if not userinfo_endpoint:
        return False
    
    # Validate token by calling userinfo endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_endpoint, headers=headers)
    
    return response.status_code == 200



async def keycloak_oauth(request: Request) -> RedirectResponse:
    try:
        user_data = await oauth.keycloak.authorize_access_token(request)  # type: ignore
    except OAuthError as e:
        print(f"OAuth error: {e}")
        return RedirectResponse(conf.url_path("/"))  # or return an error page/message
    app.storage.user["user_data"] = user_data
    return RedirectResponse(conf.url_path("/"))  # Redirect to the home page after successful login


async def logout(request: Request) -> None:
    if "user_data" in app.storage.user:
        del app.storage.user["user_data"]
    metadata =  get_metadata_keycloak()
    logout_url = metadata.get("end_session_endpoint", "")
    # Ensure the home page is accessible after logout
    u: URL = URL(logout_url)
    u = u.replace_query_params(
        **{
            "client_id": conf.OAUTH2_CLIENT_ID,
            "post_logout_redirect_uri": request.url_for("index_route"),
        }
    )
    ui.navigate.to(str(u))
