from typing import Protocol
from sqlalchemy import Select, select


class SelectBuilder(Protocol):
    def build(self) -> Select:
        pass


class ModelSelectBuilder(SelectBuilder):
    def __init__(self, model, *filters) -> None:
        self._model = model
        if not filters:
            raise ValueError("Provide at least one filter!")
        self._filters = filters

    def build(self) -> Select:
        stmt = select(self._model)
        for filter in self._filters:
            stmt.filter(filter)
        return stmt
