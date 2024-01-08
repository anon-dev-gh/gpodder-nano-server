from dependency_injector import containers, providers
from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session, sessionmaker, Session

from gpodder_nano_server.services.device import DeviceConfigurator, DevicesFetcher
from gpodder_nano_server.infra.db import NewSessionFactory


def init_session_factory(db_url):
    engine = create_engine(db_url)
    session_maker = scoped_session(sessionmaker(bind=engine))

    yield NewSessionFactory(session_maker)

    # close all sessions?


class Container(containers.DeclarativeContainer):
    # wire the modules that use "Depend"
    wiring_config = containers.WiringConfiguration(
        modules=["gpodder_nano_server.application.devices"],
    )

    # Configuration for the container
    config = providers.Configuration()

    session_factory = providers.Resource(
        init_session_factory, "sqlite://"  # FIXME: Use config to read db_url!
    )

    # Services
    devices_fetcher = providers.Factory(DevicesFetcher, session_factory)

    device_configurator = providers.Factory(DeviceConfigurator)
