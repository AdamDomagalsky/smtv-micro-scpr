import http
import logging
from unittest import mock
import pytest
from smtv_api.models import ScrapeTask

logger = logging.getLogger(__name__)

class TestEndpoints:

    @pytest.mark.parametrize(['IMG', 'TXT'], [
        (True, True),
        (False, True),
        (True, False)
    ])
    def test_post_scrape_task_created(self,app_context, test_client, db_session, IMG, TXT):

        with mock.patch(
                'smtv_api.celery_service.tasks.scrape_url.delay',
                mock.MagicMock()) as scrape_url_mock:

            url = "https://stackoverflow.com/questions/33809592/upload-to-amazon-s3-using-boto3-and-return-public-url"
            session_response = test_client.post(
                '/scrape',
                json={
                    "url": url,
                    "scrapeText": TXT,
                    "scrapeImages": IMG
                }
            )

            scrape_obj: ScrapeTask = db_session.query(ScrapeTask).first()
            assert scrape_obj.scrape_images == IMG
            assert scrape_obj.scrape_text == TXT
            scrape_url_mock.assert_called_with(id = str(scrape_obj.id))
