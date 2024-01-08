from contextlib import contextmanager
from typing import Generator
import pytest

from dependency_injector.wiring import inject
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


from gpodder_nano_server.container import Container
from gpodder_nano_server.domain import Base
from gpodder_nano_server.infra.db import SessionFactory


# A rather useful gist
# https://gist.github.com/kissgyorgy/e2365f25a213de44b9a2?permalink_comment_id=3704123


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite://")


@pytest.fixture(scope="session")
def tables(engine: Engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def dbsession(engine: Engine, tables: None):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


class ReusingSessionFactory(SessionFactory):
    def __init__(self, session: Session) -> None:
        self._session = session

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        yield self._session


@pytest.fixture
def dependency_container(request: pytest.FixtureRequest, dbsession: Session):
    container = Container()
    container.wire(modules=[request.module.__name__])
    with container.session_factory.override(ReusingSessionFactory(dbsession)):
        yield container
    container.shutdown_resources()


def injected_fixture(func):
    # Because order matters we define this combined decorator
    # See https://python-dependency-injector.ets-labs.org/wiring.html#decorator-inject
    return pytest.fixture(inject(func))
