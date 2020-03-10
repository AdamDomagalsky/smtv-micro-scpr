
import logging

from smtv_api.celery_service.celery_setup import CelerySetup

celery = CelerySetup.make_celery()
logger = logging.getLogger(__name__)


@celery.task(name='tasks.add_together')
def add_together(a: int, b: int) -> int:
    return a + b
