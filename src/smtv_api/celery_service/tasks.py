
import logging
import urllib
import os

from smtv_api.celery_service.celery_setup import CelerySetup
from smtv_api.celery_service.scraper import Scraper
from smtv_api.models import ScrapeTask, ScrapeTaskStatus
from smtv_api.helpers.file_utils import TemporaryDirectory, make_tarfile
from smtv_api import repositories
from smtv_api.storage_service import storage_s3_service
from smtv_api.settings import S3_BUCKET

celery = CelerySetup.make_celery()
logger = logging.getLogger(__name__)
ROOT_FS = '/fstorage'

@celery.task(name='add_together')
def add_together(a: int, b: int) -> int:
    return a + b


@celery.task(name='scrape_url')
@TemporaryDirectory
def scrape_url(*args, **kwargs):
    try:
        st_id = kwargs.get('id', None)
        if st_id is None:
            raise Exception('The id is none - it shouldn\'t happend - # TODO debug and fix')

        scrape_task: models.ScrapeTask = ScrapeTask.update_status(st_id, ScrapeTaskStatus.RUNNING)

        scraper = Scraper(
            scrape_id = scrape_task.id,
            scrape_text = scrape_task.scrape_text,
            scrape_images = scrape_task.scrape_images
        )

        scraper.visit_url(scrape_task.url, 0)

        scrape_task = ScrapeTask.update_status(st_id, ScrapeTaskStatus.DISPATCH)

        tar_name = f'{ROOT_FS}/{scrape_task.id}.tgz'
        make_tarfile(tar_name, source_dir = os.getcwd())
        storage_s3_service.s3_client.upload_file(tar_name, S3_BUCKET, f'{scrape_task.id}.tgz')

        scrape_task = ScrapeTask.update_status(st_id, ScrapeTaskStatus.COMPLETED)

        return str(scrape_task.id) + ' with status: ' + str(scrape_task.status.value)

    except Exception as e:
        scrape_task = ScrapeTask.update_status(st_id, ScrapeTaskStatus.FAILED, error_message=str(e))








