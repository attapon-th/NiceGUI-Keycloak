from functools import partial

from fastapi import Request
from nicegui import app, ui

from app.pkgs.config import Config, get_config
from app.pages.Auth import get_userdata

from datetime import datetime

conf: Config = get_config()


async def HomePage(request: Request) -> None:
    user_data = await get_userdata(request)
    if user_data is not None:
        ui.label(f"Hello, {user_data.get('userinfo', {}).get('name', 'User')}!").classes("text-h4")
        ui.label("You are logged in.").classes("text-h6")

        expires_at = datetime.fromtimestamp(user_data.get("expires_at"))  # type: ignore
        ui.label(f"Token expires at: {expires_at} ({expires_at - datetime.now()})").classes("text-subtitle2 my-2")
        # ui.json_editor({"content": {"json": user_data}}).classes("my-4")
        ui.button(
            "Logout",
            on_click=partial(ui.navigate.to, "/logout"),
            color="primary",
        )
    else:
        with ui.row().classes("w-full pt-12 justify-center items-center"):
            with ui.card().classes("w-full max-w-2xl "):
                ui.label("Welcome to Nicegui OAuth2!").classes("text-h4")
                ui.label("Please log in to continue.").classes("text-h6")
                ui.button(
                    "Login",
                    on_click=partial(ui.navigate.to, "/login"),
                    color="primary",
                )
