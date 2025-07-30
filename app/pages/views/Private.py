
from fastapi import Request
from nicegui import ui
from datetime import datetime
from app.pkgs.config import Config, get_config


@ui.refreshable
async def View(request: Request, _loads=False) -> None:
    conf: Config = get_config()
    # from .layout import menu
    # await menu.menu(request)

    ui.label(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}").classes("text-sm text-gray-500")
    if not _loads:
        return
    with ui.card().classes("w-full max-w-2xl"):
        ui.label("Private Page").classes("text-h4")
        ui.label("This is a private page.").classes("text-h6")
