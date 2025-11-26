from multiprocessing import freeze_support  # noqa

freeze_support()  # noqa

from typing import Optional  # noqa

from fastapi import Request  # noqa
from nicegui import app, ui  # noqa
from starlette.responses import RedirectResponse  # noqa
from app.pkgs.config import Config, get_config  # noqa
from app.pages import Auth # noqa
from app.pages.Home import HomePage  # noqa
from functools import cache
import base64


conf: Config = get_config()




@ui.page("/login", title=f"Login - {conf.APP_TITLE}")
async def login(request: Request) -> Optional[RedirectResponse]:
    return await Auth.login(request)


@app.get("/auth")
async def auth_route(request: Request) -> RedirectResponse:
    return await Auth.keycloak_oauth(request)


@ui.page("/logout")
async def logout_route(request: Request) -> RedirectResponse:
    return await Auth.logout(request)


@ui.page("/", title=f"Home - {conf.APP_TITLE}")
@ui.page("/{_}", title=f"Home - {conf.APP_TITLE}") # for sub-pages
async def index_route(request: Request) -> None:
    return await HomePage(request)


app.add_static_files("/static", "static")
app.root_path = conf.APP_BASEPATH
app.root_path_in_servers = True

@cache
def get_favicon_base64() -> str:
    with open("static/logo.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


ui.run(
    favicon=get_favicon_base64(),
    reload=conf.DEVMODE,
    host=conf.APP_HOST,
    port=conf.APP_PORT,
    title=conf.APP_TITLE,
    storage_secret=conf.APP_SECRET,
    dark=True,
    language="th",
    uvicorn_logging_level="info" if conf.DEVMODE else "warning",
)
