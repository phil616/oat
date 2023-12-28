import uvicorn
from asgi.asgi_app import asgi_application
from app_setting import config


def run_server():
    """
    run the asgi application, you can run this function in a new thread
    """
    uvicorn.run(
        asgi_application,
        host=config.ASGI_APP_HOST,
        port=config.ASGI_APP_PORT,
        reload=config.ASGI_APP_RELOAD,
    )

