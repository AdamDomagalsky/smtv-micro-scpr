import http
import logging
import uuid
from datetime import datetime
from typing import Dict, Tuple, Any

import flask
import flask_restplus
from smtv_api import database
from smtv_api import models
from smtv_api import repositories
from smtv_api import schemas

from flask_sqlalchemy import BaseQuery


logger = logging.getLogger(__name__)

blueprint = flask.Blueprint('api', __name__)
api: flask_restplus.Api = flask_restplus.Api(
    app=blueprint,
    version='0.1.0',
    default='Endpoints',
    default_label='def_label',
    title="Title",
    description="DESC")
