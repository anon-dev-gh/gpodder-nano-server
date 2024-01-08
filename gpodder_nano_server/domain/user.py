from gpodder_nano_server.domain import Base

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password: Mapped[str]  # FIXME: BRUH don't do this.
