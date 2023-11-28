"""
    filename: web_interface/asgi_config.py
    ~~~~~~~~~~~~~~~~~~~~
    config class for asgi app

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""

import dotenv
import os
import dataclasses
dotenv.load_dotenv()

@dataclasses.dataclass
class Config:
    """
    Config is a dataclass that holds the configuration of the app.
    """
    APP_NAME: str = os.getenv('APP_NAME', 'HoyoverseBoosting')
    ASGI_APP_HOST: str = os.getenv('ASGI_APP_HOST', 'localhost')
    ASGI_APP_PORT: int = int(os.getenv('ASGI_APP_PORT', 8000))
    ASGI_APP_DEBUG: bool = bool(os.getenv('ASGI_APP_DEBUG', True))
    ASGI_APP_RELOAD: bool = bool(os.getenv('ASGI_APP_RELOAD', False))
    ASGI_APP_LOG_LEVEL: str = os.getenv('ASGI_APP_LOG_LEVEL', 'info')

    MONITOR_DEBUG_SAVE: bool = bool(os.getenv('MONITOR_DEBUG_SAVE', False))

    SQLITE_DB_PATH: str = os.getenv('SQLITE_DB_PATH', './server.db')
    SQLITE_URL: str = f'sqlite://{SQLITE_DB_PATH}'

    STORAGE_PATH: str = os.getenv('STORAGE_PATH', 'storage')

    LOG_PATH: str = os.getenv('LOG_PATH', 'logs')
    
config = Config()