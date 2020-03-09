import logging
import uuid
from typing import Any

import flask_restplus
from smtv_api import models
from smtv_api import settings
from flask_restplus import fields

logger = logging.getLogger(__name__)


class UUID4(fields.String):
    __schema_type__ = "string"
    __schema_format__ = 'uuid4'
    __schema_example__ = "9d01e05b-c1b1-4061-a979-10beba9a3038"
    UUID4_PATTERN = r'^[a-fA-F0-9]{8}-([a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}$'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, pattern=self.UUID4_PATTERN, **kwargs)

    def format(self, value: uuid.UUID) -> str:
        try:
            return str(value)
        except ValueError as ve:
            raise fields.MarshallingError(ve)


S3_PATH_PATTERN = r's3://([^/]+)(/.*)?'

def init_schemas(api: flask_restplus.Api) -> None:
    for _, value in globals().items():
        if isinstance(value, flask_restplus.Model):
            api.models[value.name] = value
