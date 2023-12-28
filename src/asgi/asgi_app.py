"""
    filename: web_interface/asgi_app.py
    ~~~~~~~~~~~~~~~~~~~~
    FastAPI application for asgi server
    author: phil616
    date: 2023/11/28
    license: Apache License 2.0
"""

from fastapi import FastAPI, Request,UploadFile,File
from fastapi.responses import FileResponse
import os

from utils.local_io import a_write_file
from .asgi_events import asgi_app_lifespan
from .asgi_events import FileDB
import uuid
from .asgi_config import config

"""
DevStatus: 
1. get screenshot /// done
2. get screenshot image  /// done
3. get current input device status (mouse, keyboard)  /// done
4. send io event (mouse, keyboard)
need to construct a standard io event format

5. send a template image to find on screen
need to establish a standard template image format and file-server

"""
app = FastAPI(
    title=config.APP_NAME,
    debug=config.ASGI_APP_DEBUG,
    lifespan=asgi_app_lifespan
)


@app.get("/")
def read_root():
    return {"Hello": config.APP_NAME}


@app.get("/get/screen/monitorNumbers")
def get_screenshot(req: Request):
    numbers = req.app.state.context.device.get_screen_device_numbers()
    return {"numbers": numbers}


@app.get("/get/screen/infos")
def get_screen_infos(req: Request):
    infos = req.app.state.context.device.get_all_screen_info()
    res = []
    for info in infos:
        res.append(str(info))
    return {"infos": res}


@app.get("/get/screen/{number}/screenshot")
def get_screenshot_by_screen_id(req: Request, number: int):
    infos = req.app.state.context.device.get_all_screen_info()
    for info in infos:
        if info.capture_screen_number == number:
            req.app.state.tmpfile = True
            pic_bytes = info.capture_picture
            pic_path = os.path.join("tmp", f"{uuid.uuid4().hex}.png")
            req.app.state.context.device.screenshot_to_png(
                pic_bytes, save_path=pic_path
            )
            return FileResponse(pic_path)


@app.get("/get/io/mouse/events")
def get_mouse_position(req: Request):
    return req.app.state.context.input_listener.get_recent_mouse_events()


@app.get("/get/io/keyboard/events")
def get_keyboard_position(req: Request):
    return req.app.state.context.input_listener.get_recent_keyboard_events()


@app.get("/send/io/mouse/events")
def send_mouse_position(req: Request):
    return {"status": "not implemented"}


@app.post("/send/io/keyboard/events")
def send_keyboard_position(req: Request):
    return {"status": "not implemented"}


@app.post("/cv/find/image/scale")
def find_image_on_screen_scale(req: Request):
    return {"status": "not implemented"}


@app.post("/cv/find/image/position")
def find_image_on_screen_position(req: Request):
    return {"status": "not implemented"}


@app.post("/cv/autoclick/image")
def autoclick_image_on_screen(req: Request):
    return {"status": "not implemented"}


@app.post("/upload/file")
async def upload_file(req: Request, file: UploadFile = File(...)):
    image_file = await file.read()  # bytes
    filename = uuid.uuid4().hex     # str
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),config.STORAGE_PATH, filename)
    await a_write_file(path, image_file)
    await FileDB.create(path=path,filename=filename)
    return {"id": filename}

@app.get("/get/file/all")
async def get_all_file(req: Request):
    files = await FileDB.all()
    return files

@app.get("/get/file/{id}")
async def get_file_by_id(req: Request,fid: str):
    file = await FileDB.filter(filename=fid).first()
    return FileResponse(file.path,media_type="image/jpeg")

asgi_application = app
