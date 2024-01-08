from gpodder_nano_server.domain.user import User
from gpodder_nano_server.queries.builder import ModelSelectBuilder


class UserByUserName(ModelSelectBuilder):
    def __init__(self, username: str) -> None:
        super().__init__(User, User.name == username)
