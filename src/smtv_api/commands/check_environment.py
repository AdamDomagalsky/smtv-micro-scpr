import io
import logging
import tempfile
from typing import Callable

import botocore
import requests
from sqlalchemy import exc

from smtv_api import database
from smtv_api import settings
from smtv_api.flask_app import create_app
from smtv_api.storage_service.storage_s3_service import s3_client

logger = logging.getLogger(__name__)


class HealthCheckRegistry(object):
    def __init__(self) -> None:
        self.registry: dict = {}
        self.function_results: dict = {}
        self.failed_counter = 0

    def __call__(self, func: Callable) -> None:
        self.registry[func.__name__] = func
        self.function_results[func.__name__] = False

    def execute(self) -> bool:
        passed = True
        for func in self.registry:
            result = self.registry[func]()
            self.function_results[func] = result
            if result:
                logger.info(f'[OK]\u2713 {func}')
            else:
                logger.error(f'[FAILED]\u2717 {func}')
                self.failed_counter += 1
            passed &= result

        if passed:
            return True
        else:
            return False


healthcheck_registry = HealthCheckRegistry()

@healthcheck_registry
def s3_internal_bucket_health_check() -> bool:
    with tempfile.TemporaryFile() as outFile:
        try:
            test_string = 'This is a test string'
            tmpFile = io.BytesIO(test_string.encode())
            file_name = 'fileName.txt'
            s3_client.create_bucket(Bucket=settings.S3_BUCKET)
            s3_client.upload_fileobj(tmpFile, settings.S3_BUCKET, file_name)
            s3_client.download_fileobj(settings.S3_BUCKET, file_name, outFile)
            s3_client.delete_object(
                Bucket=settings.S3_BUCKET,
                Key=file_name
            )

            outFile.seek(0)
            if not outFile.readline().decode() == test_string:
                logger.warning('s3bucket: Downloaded content of the file is other than uploaded')
                return False

        except botocore.exceptions.ClientError:
            logger.exception('s3bucket:')
            return False

    return True


@healthcheck_registry
def postgres_health_check() -> bool:
    try:
        database.db.session.execute('SELECT 1')
    except exc.SQLAlchemyError:
        logger.exception('postgres failed')
        return False

    return True


def run() -> None:
    app = create_app()
    with app.app_context():
        if healthcheck_registry.execute():
            logger.info('HEALTH CHECK PASSED')
            exit(0)
        else:
            logger.error(
                f'{healthcheck_registry.failed_counter}/'
                f'{len(healthcheck_registry.function_results)} HEALTH CHECKS FAILED!'
            )
            exit(1)


if __name__ == '__main__':
    run()
