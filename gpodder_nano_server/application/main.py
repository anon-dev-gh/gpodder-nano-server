from fastapi import FastAPI
from gpodder_nano_server.application import devices
from gpodder_nano_server.containers.device import DeviceContainer

def create_app() -> FastAPI:
    app = FastAPI()
    # TODO:  I don't know why I have to instantiate the container manually.
    device_container = DeviceContainer()
    app.include_router(devices.router)

    return app
