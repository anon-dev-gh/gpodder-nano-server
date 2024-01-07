from typing import Iterable
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from pydantic import BaseModel

from gpodder_nano_server.containers.device import DeviceContainer
from gpodder_nano_server.domain.device import Device
from gpodder_nano_server.domain.user import User
from gpodder_nano_server.services.device import DevicesFetcher

router = APIRouter()

class DeviceModel(BaseModel):
    id: int

@router.get("/api/2/devices/{username}.json")
@inject
async def fetch_devices(
    username: str,
    devices_fetcher: DevicesFetcher = Depends(Provide[DeviceContainer.devices_fetcher]),
) -> Iterable[DeviceModel]:
    devices = await devices_fetcher.fetch_devices(User())
    return map(map_device_to_device_model, devices)


def map_device_to_device_model(device: Device) -> DeviceModel:
    return DeviceModel(id=device.id)
