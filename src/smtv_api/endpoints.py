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
from smtv_api import helpers

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


@api.route('/scrape')
class ScrapeUrl(flask_restplus.Resource):
    @api.expect(schemas.SCRAPE_URL, validate=True)
    @api.marshal_with(
        schemas.SCRAPE_URL,
        skip_none=True,
        code=201,
        description='Created - scrape task created based on url',
    )
    def post(self) -> Tuple[models.ScrapeTask, http.HTTPStatus]:
        payload = helpers.get_payload(schemas.SCRAPE_URL)


        scrape_repository = repositories.ScrapeTaskStatusRepository()
        scrape_task: models.ScrapeTask = scrape_repository.create(payload)

        return scrape_task, http.HTTPStatus.CREATED

@api.route('/scrape/<uuid:id>/status')
class CheckScrape(flask_restplus.Resource):
    @api.marshal_with(
        schemas.SCRAPE_URL,
        skip_none=False,
        code=202,
        description='OK - returns scrape task details'
    )
    @api.response(
        404,
        "Not found - scrape task '{id}' not found"
    )
    @api.doc(params={'id': 'scrape task id from POST /scrape'})
    def get(self, id: uuid.UUID) -> Tuple[models.ScrapeTask, http.HTTPStatus]:
        scrape_repository = repositories.ScrapeTaskStatusRepository()
        scrape_task: models.ScrapeTask = scrape_repository.get(id)
        return scrape_task, http.HTTPStatus.OK


@api.route('/scrape/<uuid:id>/download')
class CheckScrape(flask_restplus.Resource):
    @api.marshal_with(
        schemas.SCRAPE_URL,
        skip_none=False,
        code=200,
        description='OK - returns scrape task details'
    )
    @api.response(
        202,
        "Accepted - however task not finished yet, therefore empty downloadUrl"
    )
    @api.response(
        204,
        "No Content - scrape task finished, but error occured or no result"
    )
    @api.doc(params={'id': 'scrape task id from POST /scrape'})
    def get(self, id: uuid.UUID) -> Tuple[models.ScrapeTask, http.HTTPStatus]:
        scrape_repository = repositories.ScrapeTaskStatusRepository()
        scrape_task: models.ScrapeTask = scrape_repository.get(id)

        ret_http_status = http.HTTPStatus.OK
        ret_http_status = http.HTTPStatus.NO_CONTENT
        ret_http_status = http.HTTPStatus.ACCEPTED


        return scrape_task, ret_http_status

