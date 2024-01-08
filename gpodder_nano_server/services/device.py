from typing import Iterable

from gpodder_nano_server.domain.device import Device
from gpodder_nano_server.domain.user import User
from gpodder_nano_server.infra.db import SessionFactory
from gpodder_nano_server.queries.user import UserByUserName


class DevicesFetcher:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def fetch_devices(self, username: str) -> Iterable[Device]:
        stmt = UserByUserName(username).build()

        with self._session_factory.session() as session:
            user = session.execute(stmt).one_or_none()

        if user is None:
            raise ValueError("User not found")

        return user.devices

class DeviceConfigurator:
    def configure_device(self, user: User, device: Device) -> None:
        pass
