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
from smtv_api.celery_service import tasks as celery_tasks

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

def check_head_url_exist(url):
    try:
        import httplib2
        h = httplib2.Http()
        resp = h.request(url, 'HEAD')
        reutrn_code = int(resp[0]['status'])

        if reutrn_code >= 400:
            if reutrn_code == 403:
                return
            helpers.error_abort(
                    code=http.HTTPStatus.BAD_REQUEST,
                    message = f'Given url does not exist or some problem occured getting.'
                    f' Got code:{reutrn_code} when HEAD {url}'
                )

    except (httplib2.ServerNotFoundError, OSError):
        helpers.error_abort(
                code=http.HTTPStatus.BAD_REQUEST,
                message = f'Given url does not exist: {url}'
            )


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

        if not payload['scrape_text'] and not payload['scrape_images']:
            helpers.error_abort(
                code=http.HTTPStatus.NOT_ACCEPTABLE,
                message = 'No effect of the task - at least one of scrape text or images have to be True'
            )

        check_head_url_exist(payload['url'])


        scrape_repository = repositories.ScrapeTaskRepository()
        scrape_task: models.ScrapeTask = scrape_repository.create(payload)
        
        result = celery_tasks.scrape_url.delay(id = str(scrape_task.id))

        # helpers.error_abort(
        #     code=http.HTTPStatus.NOT_IMPLEMENTED,
        #     message= result.wait()
        # )

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
        scrape_repository = repositories.ScrapeTaskRepository()
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
        scrape_repository = repositories.ScrapeTaskRepository()
        scrape_task: models.ScrapeTask = scrape_repository.get(id)

        ret_http_status = http.HTTPStatus.OK
        ret_http_status = http.HTTPStatus.NO_CONTENT
        ret_http_status = http.HTTPStatus.ACCEPTED


        return scrape_task, ret_http_status

# TMP to test celery connection
@api.route('/add')
class AddTgther(flask_restplus.Resource):
    def get(self) -> Tuple[Dict[str, Any], http.HTTPStatus]:
        payload = flask.request.json
        a = b = 1
        if payload:
            a = payload.get("a", 1)
            b = payload.get("b", 1)
        result = celery_tasks.add_together.delay(a, b)
        # https://github.com/celery/celery/pull/5931 ISSUE ... downgrade celery 4.4.1 to 4.4.0
        return {
            'a+b=': result.wait(),
            'a': a,
            'b': b
        }, http.HTTPStatus.OK

