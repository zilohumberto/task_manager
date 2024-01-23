from typing import Optional, Sequence

from application.models.models import db

Model = db.Model


class BaseRepository:
    def get(self, pk: str) -> Optional[Model]:
        raise NotImplementedError()

    def create(self, obj: Model) -> Optional[Model]:
        raise NotImplementedError()

    def filter(self, **kwargs) -> Sequence[Model]:
        raise NotImplementedError()

    def delete(self, **kwargs):
        raise NotImplementedError()

    def save(self, obj: Model):
        raise NotImplementedError()
