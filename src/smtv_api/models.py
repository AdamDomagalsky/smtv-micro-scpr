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
