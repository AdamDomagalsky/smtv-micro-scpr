import http
import logging
import typing

import flask

from smtv_api import database
from smtv_api import endpoints
from smtv_api import schemas

from smtv_api import settings


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)
    app.config.from_object(settings)
    init_logging()
    database.db.init_app(app)
    return app


def create_web_app() -> flask.Flask:
    app = create_app()
    init_healthcheck(app)
    init_api(app)
    return app


def init_healthcheck(app: flask.Flask) -> None:
    @app.route('/healthz')
    def empty_response() -> typing.Tuple[str, int]:
        return '', http.HTTPStatus.NO_CONTENT


def init_api(app: flask.Flask) -> None:
    app.register_blueprint(endpoints.blueprint)
    # if you'd like to check url's availabe
    # raise Exception(app.url_map)
    schemas.init_schemas(endpoints.api)


def init_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        format='%(levelname)s %(asctime)s %(name)s - %(message)s',
    )
