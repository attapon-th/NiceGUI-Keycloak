from functools import partial

from fastapi import Request
from nicegui import ui

from app.pkgs.config import Config, get_config
from app.pages.Auth import get_userdata

from datetime import datetime

conf: Config = get_config()


def navigate_to(path: str):
    return lambda: ui.navigate.to(path)


async def HomePage(request: Request) -> None:
    user_data = await get_userdata(request)
    if user_data is not None:
        # with ui.header().classes("bg-transparent items-center py-2"):
        #     ui.avatar("favorite_border")
        #     ui.label(conf.APP_TITLE).classes("text-h5 ml-2")
        with ui.left_drawer().classes(" items-start"):
            with ui.row().classes("w-full items-center"):
                ui.avatar("img:./static/logo.png").classes("ml-2")
                ui.label(conf.APP_TITLE).classes("text-h5 ml-2")
            ui.separator()
            ui.button("Home", on_click=navigate_to("/"), color="primary", icon="home").props("flat").classes("w-full items-start")
            ui.separator()
            # menu
            ui.button(
                "Private",
                icon="lock",
                on_click=navigate_to("/private"),
                color="secondary",
            ).props("flat").classes("w-full items-start")
            with ui.row().classes("w-full mt-auto px-4 py-2 items-start"):
                ui.separator()
                userinfo = user_data.get("userinfo", {})
                ui.markdown(f"Logged in as `{userinfo.get('preferred_username', 'User')}`  \nName: `{userinfo.get('name', 'User')}`").classes("text-subtitle2")
                ui.button("Logout", on_click=navigate_to("/logout"), color="negative", icon="logout").classes("w-full items-start mt-auto")
                ui.separator()
        # with ui.footer().classes("bg-primary mt-12 items-center align-center py-1"):
        #     ui.label(f"© {datetime.now().year} {conf.APP_TITLE}").classes("text-white")

        # add sub-page view
        from app.pages.Private import ViewPrivate
        
        ui.sub_pages(
            {
                "/": lambda: ViewIndex(request, user_data),
                "/private": lambda: ViewPrivate(request),
            }
        ).classes("mt-4 w-full")

    else:
        await ViewNoLogin()


async def ViewNoLogin():
    with ui.row().classes("w-full pt-12 justify-center items-center"):
        with ui.card().classes("w-full max-w-2xl mx-auto"):
            ui.label("Welcome to Nicegui OAuth2!").classes("text-h4")
            ui.label("Please log in to continue.").classes("text-h6")
            ui.button(
                "Login",
                on_click=partial(ui.navigate.to, "/login"),
                color="primary",
            )


async def ViewIndex(request: Request, user_data: dict) -> None:
    with ui.row().classes("w-full justify-center items-center"):
        with ui.card().classes("w-full h-full mx-auto"):
            ui.label(f"Hello, {user_data.get('userinfo', {}).get('name', 'User')}!").classes("text-xl")
            ui.label("You are logged in.").classes("text-h6")

            expires_at = datetime.fromtimestamp(user_data.get("expires_at"))  # type: ignore
            ui.label(f"Token expires at: {expires_at} ({expires_at - datetime.now()})").classes("text-subtitle2 my-2")
            # ui.json_editor({"content": {"json": user_data}}).classes("my-4")
            # ui.button("Logout", on_click=navigate_to("/logout"), color="negative", icon="logout")


