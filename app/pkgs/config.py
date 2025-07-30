import os
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from nicegui import ui

@dataclass
class Config:
    DEVMODE: bool
    OAUTH2_CLIENT_ID: str
    OAUTH2_CLIENT_SECRET: str
    OAUTH2_METADATA_URL: str
    APP_HOST: str
    APP_PORT: int
    APP_SECRET: str
    APP_BASEPATH: str

    PROJECT_PATH: Path
    STORAGE_PATH: Path

    APP_TITLE: str = "NiceGUI App"

    def __init__(self):
        self.DEVMODE = os.getenv("DEVMODE", "1").lower() == "1"
        self.OAUTH2_CLIENT_ID = os.getenv("OAUTH2_CLIENT_ID", "")
        self.OAUTH2_CLIENT_SECRET = os.getenv("OAUTH2_CLIENT_SECRET", "")
        self.OAUTH2_METADATA_URL = os.getenv("OAUTH2_METADATA_URL", "")
        self.APP_PORT = int(os.getenv("APP_PORT", 8080))
        self.APP_HOST = os.getenv("APP_HOST", "localhost")
        self.APP_SECRET = os.getenv("APP_SECRET", "")
        self.APP_BASEPATH = os.getenv("APP_BASEPATH", "/nicegui")

        self.PROJECT_PATH = Path(os.getenv("PROJECT_PATH", "."))
        self.STORAGE_PATH = Path(os.getenv("STORAGE_PATH", "storage"))
        self.STORAGE_PATH.mkdir(parents=True, exist_ok=True)

        


    # def url_path(self, path: str) -> str:
    #     """
    #     Constructs a full URL path by joining the APP_BASEPATH with the provided path.
    #     """
    #     u = f"{self.APP_BASEPATH}{path}"
    #     return u
    
    # def navigate_to(self, path: str) -> None:
    #     ui.navigate.to(self.url_path(path))
        

        

@cache
def get_config() -> Config:
    """
    Returns a singleton instance of the Config class.
    This function caches the instance to avoid creating multiple instances.
    """
    return Config()
