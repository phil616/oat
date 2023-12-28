from dataclasses import dataclass

@dataclass
class AppSetting:
    ASGI_APP_HOST = "127.0.0.1"
    ASGI_APP_PORT = 8000
    ASGI_APP_RELOAD = True


config = AppSetting()
