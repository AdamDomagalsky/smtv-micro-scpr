import enum
import logging
from datetime import datetime
from typing import Dict
from typing import List
from typing import Any
from typing import Tuple

import sqlalchemy as sa
from smtv_api import database
from smtv_api import settings
from smtv_api.storage_service import storage_s3_service
from flask_sqlalchemy import BaseQuery
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref
from sqlalchemy.util import KeyedTuple

logger = logging.getLogger(__name__)

Base = declarative_base()


class ScrapeTaskStatus(enum.Enum):
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    DISPATCH = 'DISPATCH'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

class ScrapeTask(database.db.Model):
    __tablename__ = "scrape_task"

    id = sa.Column(postgresql.UUID(as_uuid=True), server_default=sa.text("uuid_generate_v4()"), primary_key=True)
    created_at = sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False)
    start_date = sa.Column(sa.DateTime, default=None, nullable=True)
    ended_at = sa.Column(sa.DateTime, default=None, nullable=True)

    url = sa.Column(sa.String, nullable=False)
    scrape_text = sa.Column(sa.Boolean, default=True)
    scrape_images = sa.Column(sa.Boolean, default=True)
    status = sa.Column(sa.Enum(ScrapeTaskStatus), default=ScrapeTaskStatus.PENDING, nullable=False, index=True)
    error_message = sa.Column(sa.String(), nullable=True)

    @classmethod
    def update_status(cls, id, status: ScrapeTaskStatus, error_message = None):
        from smtv_api.repositories import ScrapeTaskRepository

        scrape_repository = ScrapeTaskRepository()
            
        data = {
            'status': status
        }

        if status == ScrapeTaskStatus.RUNNING:
            data['start_date'] = sa.func.now()
        elif status == ScrapeTaskStatus.COMPLETED:
            data['ended_at'] = sa.func.now()
        elif error_message:
            data['ended_at'] = sa.func.now()
            data['error_message'] = error_message

        updated_scrape_task = scrape_repository.update(
            id = id,
            data = data
        )

        return updated_scrape_task

    @property
    def download_link(self):
        if self.status != ScrapeTaskStatus.COMPLETED:
            return None

        url = storage_s3_service.s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.S3_BUCKET,
                'Key': f'{self.id}.tgz'
            }
        )

        # TODO 4 dev only, won't affect prod and real s3
        return url.replace('localstack', 'localhost')


