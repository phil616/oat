"""
    filename: web_interface/asgi_app.py
    ~~~~~~~~~~~~~~~~~~~~
    FastAPI application for asgi server

    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""

import shutil
import threading
import fastapi
import contextlib
from io_tools import device
import os
from tortoise.models import Model
from tortoise import fields,Tortoise
from utils.background import monitor_directory
from .asgi_config import config


class FileDB(Model):
    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=255)
    path = fields.CharField(max_length=255)

    class Meta:
        table = "filedb"
        description = "file database"


class AsgiContext:
    """
    AsgiContext is a singleton class that holds the context of the ASGI app.

    It is used to store the device and input listener instances.
    """
    _instance = None

    def __new__(cls):
        if AsgiContext._instance is None:
            AsgiContext._instance = object.__new__(cls)
        return AsgiContext._instance

    def __init__(self) -> None:
        self.device = device.DeviceOperate()
        self.input_listener = device.InputListener()
        self.input_listener.start()

@contextlib.asynccontextmanager
async def asgi_app_lifespan(app: fastapi.FastAPI):
    """
    A context manager that handles the lifespan of an ASGI app.
    """
    # init context
    context = AsgiContext()
    await Tortoise.init(
        db_url=config.SQLITE_URL,
        modules={'models': [__name__]}
    )

    await Tortoise.generate_schemas()

    # mount context to app
    app.state.context = context
    storage_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),config.STORAGE_PATH)

    if not os.path.exists(storage_path):
        os.mkdir(storage_path)
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    # clean tmp directory
    threading.Thread(target=monitor_directory, args=("tmp",), daemon=True).start()

    yield  # wait for app to finish

    # in StreamResponse or FileResponse, the response will be closed automatically
    # however we don't know when the response is closed, so we can't delete the tmp file immediately
    shutil.rmtree('tmp')
    context.input_listener.stop()
    # close database connection
    await Tortoise.close_connections()
