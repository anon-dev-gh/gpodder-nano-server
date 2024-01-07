import pytest
from dependency_injector.wiring import inject

from gpodder_nano_server.containers.device import DeviceContainer

@pytest.fixture(autouse=True)
def device_container(request: pytest.FixtureRequest):
    container = DeviceContainer()
    container.init_resources()
    container.wire(modules=[request.module.__name__])
    return container


def injected_fixture(func):
    # Because order matters we define this combined decorator
    # See https://python-dependency-injector.ets-labs.org/wiring.html#decorator-inject
    return pytest.fixture(inject(func))