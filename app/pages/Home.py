from functools import partial

from fastapi import Request
from nicegui import app, ui

from app.pages import Auth
from app.pkgs.config import Config, get_config
from dataclasses import dataclass
from typing import Callable
from typing import Optional

from fastapi.datastructures import URL
from starlette.responses import RedirectResponse
from datetime import datetime

conf: Config = get_config()

@dataclass
class MenuItem:
    name: str
    label: str
    icon: str
    page: Callable


async def get_userdata() -> Optional[dict]:
    try:
        return app.storage.user["user_data"]
    except Exception:
        return None


async def login(request: Request) -> Optional[RedirectResponse]:
    user_data = await get_userdata()
    if user_data:
        return RedirectResponse("/")
    else:
        ui.label("Welcome to Nicegui!")
        ui.label("Please log in to continue.")

        url: URL = request.url_for("auth_route")
        return await Auth.authorize_redirect(request, redirect_uri=url)  # type: ignore
@ui.refreshable
async def _home(request: Request) -> None:
    user_data = await get_userdata()
    if user_data:
        ui.label(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}").classes("text-sm text-gray-500")

        ui.label(f"Welcome {user_data.get('userinfo', {}).get('name', '')}!").classes("text-h4")
        ui.label("This is the home page.").classes("text-h6")
        ui.button("Logout", on_click=lambda: Auth.logout(request), color="negative")



async def HomePage(request: Request) -> None:
    if not await Auth.check_access_token():
        try:
            app.storage.user["user_data"] = None
        except Exception:
            pass

    user_data = await get_userdata()
    
    if user_data:
        # await menu(request)
        from app.pages.views import (
            Private
        )
        menus = [
            MenuItem(name='Home', label='Home', icon='home', page=_home),
            MenuItem(name='Private', label='Private', icon='thumb_up', page=Private.View)
        ]
        with ui.header(fixed=False).classes(replace="bg-neutral-800 row p-0 px-4"):
            with ui.link(target=conf.url_path("/")).classes("flex items-center"):
                ui.image(
                    conf.url_path("/static/logo.png")  # Replace with your logo path
                ).classes("w-12 h-12 rounded-full p-2  my-1 mr-4")
            with ui.tabs() as tabs:
                for menu in menus:
                    ui.tab(menu.name, menu.label, icon=menu.icon)

        # Handle tab change and refresh the page
        async def handle_tab_change(event):
            for menu in menus:
                if event.value == menu.name:
                    with ui.tab_panel(menu.name):
                        menu.page.refresh()
                        break
        with ui.tab_panels(tabs, value='Home', animated=False, keep_alive=False, on_change=handle_tab_change).classes('w-full'):
            for menu in menus:
                with ui.tab_panel(menu.name) :
                    await menu.page(request)


        # panels.on('change', handle_tab_change)
        # ui.json_editor({"content": {"json": auth.get_metadata_keycloak()}})
    else:
        with ui.row().classes("w-full pt-12 justify-center items-center"):
            with ui.card().classes("w-full max-w-2xl "):
                ui.label("Welcome to Nicegui OAuth2!").classes("text-h4")
                ui.label("Please log in to continue.").classes("text-h6")
                ui.button(
                    "Login",
                    on_click=partial(ui.navigate.to, conf.url_path("/login")),
                    color="primary",
                )


