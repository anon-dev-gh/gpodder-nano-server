from dependency_injector import containers, providers
from gpodder_nano_server.services import device


class DeviceContainer(containers.DeclarativeContainer):   
    wiring_config = containers.WiringConfiguration(
        modules=["gpodder_nano_server.application.devices"],
    )

    devices_fetcher = providers.Factory(
        device.DevicesFetcher
    )

    device_configurator = providers.Factory(
        device.DeviceConfigurator
    )


