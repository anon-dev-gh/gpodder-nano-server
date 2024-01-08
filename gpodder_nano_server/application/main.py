from fastapi import FastAPI
from gpodder_nano_server.application import devices
from gpodder_nano_server.container import Container


def create_app() -> FastAPI:
    app = FastAPI()
    Container()
    app.include_router(devices.router)

    return app
