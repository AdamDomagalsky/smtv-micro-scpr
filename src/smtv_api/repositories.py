import abc
import http
import logging
import typing
import uuid

from smtv_api import database
from smtv_api import helpers
from smtv_api import models
from sqlalchemy import exc
from sqlalchemy import orm
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import exc as orm_exc

logger = logging.getLogger(__name__)

Model = typing.TypeVar('Model', bound=database.db.Model)


class ModelRepository(abc.ABC):
    @property
    @abc.abstractmethod
    def model(self) -> typing.Type[Model]:
        pass

    def create(self, data: typing.Dict[str, typing.Any]) -> Model:
        try:
            object_: Model = self.model(**data)
            database.db.session.add(object_)
            database.db.session.commit()
        except exc.SQLAlchemyError:
            logger.exception(f'Create ModelRepository({self.model.__name__})')
            helpers.error_abort(
                code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
                message=f"Creation of '{self.model.__name__}' failed"
            )
        return object_

    def create_all(self, data: typing.List[typing.Dict[str, typing.Any]]) -> None:
        try:
            for model_definition in data:
                object_: Model = self.model(**model_definition)  # type: ignore
                database.db.session.add(object_)

            database.db.session.commit()
        except exc.SQLAlchemyError:
            logger.exception(f'Create ModelRepository({self.model.__name__})')
            helpers.error_abort(
                code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
                message=f"Creation of '{self.model.__name__}' failed"
            )

    def _check_model_property(self, object_: Model, key: str) -> bool:
        mapper = class_mapper(object_.__class__).get_property(key)
        if (isinstance(mapper, orm.ColumnProperty) or isinstance(mapper, orm.RelationshipProperty)):
            return True
        else:
            return False

    def update(self, id: uuid.UUID, data: typing.Dict[str, typing.Any]) -> Model:
        try:
            object_: Model = self.get(id)

            for key, value in data.items():
                if not self._check_model_property(object_, key):
                    raise RepositoryError
                setattr(object_, key, value)

            database.db.session.add(object_)
            database.db.session.commit()

        except exc.SQLAlchemyError:
            logger.exception(f'Update ModelRepository({self.model.__name__})')
            helpers.error_abort(
                code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
                message=f"Update of '{self.model.__name__}' failed"
            )

        return object_

    def get(self, id: uuid.UUID, with_for_update: bool = False) -> Model:
        try:
            query = (
                database.db.session
                .query(self.model)
                .filter_by(id=id)
            )

            if with_for_update:
                query = query.with_for_update(of=self.model)

            objects_: Model = query.one()

        except orm_exc.NoResultFound:
            helpers.error_abort(
                code=http.HTTPStatus.NOT_FOUND,
                message=f"'{self.model.__name__}' not found"
            )
        return objects_

class ScrapeTaskStatusRepository(ModelRepository):
    model = models.ScrapeTask


class RepositoryError(Exception):
    pass
