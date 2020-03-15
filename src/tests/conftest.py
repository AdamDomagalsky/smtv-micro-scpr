import logging

import pytest

from smtv_api import database

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def app():
    from smtv_api import flask_app
    return flask_app.create_web_app()


@pytest.fixture(scope='session')
def app_context(app):
    with app.test_request_context():
        yield


@pytest.fixture(scope='session')
def test_client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope='session')
def _db(app):
    return database.db
