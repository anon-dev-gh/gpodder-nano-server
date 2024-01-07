import pytest
from gpodder_nano_server.domain.device import Device
from gpodder_nano_server.domain.user import User
from gpodder_nano_server.services.device import DeviceConfigurator, DevicesFetcher


from dependency_injector.wiring import inject, Provide
from gpodder_nano_server.containers.device import DeviceContainer
from test.conftest import injected_fixture


@injected_fixture
def devices_fetcher(
    devices_fetcher: DevicesFetcher = Provide[DeviceContainer.devices_fetcher],
):
    return devices_fetcher

def test_devices_fetcher_fetch_devices(
    devices_fetcher
):
    user = User()
    devices = devices_fetcher.fetch_devices(user)
    assert devices == user.devices


@injected_fixture
def device_configurator(
    device_configurator: DeviceConfigurator = Provide[DeviceContainer.device_configurator],
):
    return device_configurator

def test_device_configurator(device_configurator: DeviceConfigurator):
    user = User()
    device = Device()
    device_configurator.configure_device(user, device)

    assert device
