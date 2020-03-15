import logging
import uuid
from typing import Any
import re
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
# TODO smthing doesnt work with flask resplus
DJANGO_URL_VALIDATION_REGEX = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


SCRAPE_URL = flask_restplus.Model('ScrapeUrl',{
    'scrapeID': UUID4(readonly=True, attribute='id'),
    'url': fields.String(
        # required=True,
        # pattern=DJANGO_URL_VALIDATION_REGEX.pattern,
        description='Valid URLs: HTTP, HTTPS & FTP. Rest prefx is malformed'),
    'scrapeText': fields.Boolean(default=True, attribute='scrape_text'),
    'scrapeImages': fields.Boolean(default=True, attribute='scrape_images'),
    'status': fields.String(
        enum=[status.value for status in models.ScrapeTaskStatus],
        readonly=True,
        attribute=lambda x: x.status.value),
    'createTime': fields.DateTime(readonly=True, allow_null=True, attribute='created_at'),
    'startDate': fields.DateTime(readonly=True, allow_null=True, attribute='start_date'),
    'endTime': fields.DateTime(readonly=True, allow_null=True, attribute='ended_at'),
    'errorMessage': fields.String(readonly=True, allow_null=True, attribute='error_message'),
    'downloadLink': fields.String(readonly=True, allow_null=True, attribute='download_link'),
})


def init_schemas(api: flask_restplus.Api) -> None:
    for _, value in globals().items():
        if isinstance(value, flask_restplus.Model):
            api.models[value.name] = value
