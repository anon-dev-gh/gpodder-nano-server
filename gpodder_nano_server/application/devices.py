from typing import Iterable
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dependency_injector.wiring import Provide, inject

from gpodder_nano_server.domain.device import Device
from gpodder_nano_server.container import Container
from gpodder_nano_server.services.device import DevicesFetcher

router = APIRouter()

class DeviceModel(BaseModel):
    id: int
    user_id: int

@router.get("/api/2/devices/{username}.json")
@inject
async def fetch_devices(
    username: str,
    devices_fetcher: DevicesFetcher = Depends(Provide[Container.devices_fetcher]),
) -> Iterable[DeviceModel]:
    devices = devices_fetcher.fetch_devices(username)
    return map(map_device_to_device_model, devices)


def map_device_to_device_model(device: Device) -> DeviceModel:
    return DeviceModel(id=device.id, user_id=device.user_id)
