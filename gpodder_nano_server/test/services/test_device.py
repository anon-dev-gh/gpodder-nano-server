from dependency_injector.wiring import Provide
from gpodder_nano_server.domain.device import Device
from gpodder_nano_server.domain.user import User
from gpodder_nano_server.container import Container

from gpodder_nano_server.services.device import DeviceConfigurator, DevicesFetcher
from gpodder_nano_server.test.conftest import injected_fixture


@injected_fixture
def devices_fetcher(
    dependency_container,
    devices_fetcher: DevicesFetcher = Provide[Container.devices_fetcher],
):
    return devices_fetcher


def test_devices_fetcher_fetch_devices(devices_fetcher: DevicesFetcher):
    user = User()
    devices = devices_fetcher.fetch_devices(user.name)
    assert devices


@injected_fixture
def device_configurator(
    dependency_container,
    device_configurator: DeviceConfigurator = Provide[Container.device_configurator],
):
    return device_configurator


def test_device_configurator(device_configurator: DeviceConfigurator):
    user = User()
    device = Device()
    device_configurator.configure_device(user, device)

    assert device
