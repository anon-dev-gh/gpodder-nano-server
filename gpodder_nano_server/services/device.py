from typing import Iterable
from gpodder_nano_server.domain.device import Device
from gpodder_nano_server.domain.user import User


class DevicesFetcher:
    def fetch_devices(self, username: str) -> Iterable[Device]:
        return user.devices
    
class DeviceConfigurator:
    def configure_device(self, user: User, device: Device) -> None:
        pass
