from typing import Optional

from fastapi import Request
from nicegui import app, ui
from starlette.responses import RedirectResponse
from app.pkgs.config import Config, get_config
from app.pages import Auth
from app.pages.Home import HomePage, login as HomeLogin

conf: Config = get_config()


@ui.page(conf.url_path("/login"), title="Login - Nicegui OAuth2")
async def login(request: Request) -> Optional[RedirectResponse]:
    return await HomeLogin(request)


@app.get(conf.url_path("/auth")) 
async def auth_route(request: Request) -> RedirectResponse:
    return await Auth.keycloak_oauth(request)

@app.get(conf.url_path("/logout"))
async def logout_route(request: Request) -> None:
    return await Auth.logout(request)


@ui.page(conf.url_path("/"), title="Home - Nicegui OAuth2")
async def index_route(request: Request) -> None:
    return await HomePage(request)


if conf.url_path("/") != "/":
    @ui.page("/")
    async def redirect_to_home(request: Request) -> RedirectResponse:
        return RedirectResponse(conf.url_path("/"))




app.add_static_files(conf.url_path("/static"), "static")
ui.run(
    host=conf.APP_HOST,
    port=conf.APP_PORT,
    title="Nicegui",
    storage_secret=conf.APP_SECRET,
    dark=True,
    language="th",
    uvicorn_logging_level="debug"
)
