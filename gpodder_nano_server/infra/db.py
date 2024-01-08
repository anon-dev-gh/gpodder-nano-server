from collections.abc import Generator
from contextlib import contextmanager
import logging
from typing import Protocol
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

logger = logging.getLogger(__name__)


class SessionFactory(Protocol):
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        pass


class NewSessionFactory(SessionFactory):
    def __init__(self, session_factory: scoped_session) -> None:
        self._session_factory = session_factory

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Unexpected error, rollback")
            session.rollback()
            raise
        finally:
            session.close()
