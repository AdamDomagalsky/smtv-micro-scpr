import enum
import logging
from datetime import datetime
from typing import Dict
from typing import List
from typing import Any
from typing import Tuple

import sqlalchemy as sa
from smtv_api import database
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
    PENDING_PLAIN_CELERY = 'PENDING_PLAIN_CELERY'
    RUNNING_PLAIN_CELERY = 'RUNNING_PLAIN_CELERY'
    FAILED_PLAIN_CELERY = 'FAILED_PLAIN_CELERY'
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
    download_link = sa.Column(sa.String(), nullable=True)
