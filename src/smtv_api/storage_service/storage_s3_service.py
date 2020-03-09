import logging

from typing import Any
from typing import Dict

import boto3
import botocore

from smtv_api import settings
from smtv_api.storage_service import storage_abstract

logger = logging.getLogger(__name__)

try:
    s3_client = boto3.client(
        service_name='s3',
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        endpoint_url=settings.S3_ENDPOINT_URL
    )
except Exception:
    logger.exception('s3_client connection error')


class S3Service(storage_abstract.StorageServiceABC):

    @classmethod
    def get_object_url(cls, key_name: str, bucket_name: str) -> str:
        raise NotImplementedError
