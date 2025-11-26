
from fastapi import Request
from nicegui import ui
from datetime import datetime
# from app.pkgs.config import Config, get_config


async def ViewPrivate(request: Request) -> None:

    ui.label(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}").classes("text-sm text-gray-500")
    with ui.card().classes("w-full mx-auto"):
        ui.label("Private Page").classes("text-h4")
        ui.label("This is a private page.").classes("text-h6")
