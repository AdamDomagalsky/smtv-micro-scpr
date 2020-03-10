from typing import Any

from celery import Celery
from smtv_api import database
from smtv_api import settings
from flask import Flask


class CelerySetup:
    flask_app = Flask(__name__)
    flask_app.config.from_object(settings)
    flask_app.config.update(
        CELERY_BROKER_URL=settings.CELERY_BROKER_URL,
        CELERY_RESULT_BACKEND=settings.CELERY_RESULT_BACKEND
    )

    @classmethod
    def make_celery(cls) -> Any:
        '''

        :return: decorator: celery
        '''
        app = cls.flask_app
        database.db.init_app(app)
        celery = Celery(
            app.import_name,
            backend=app.config['CELERY_RESULT_BACKEND'],
            broker=app.config['CELERY_BROKER_URL']
        )
        celery.conf.update(app.config)

        class ContextTask(celery.Task):  # type: ignore
            def __call__(self, *args, **kwargs):  # type: ignore
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery.Task = ContextTask
        return celery

# celery = CelerySetup.make_celery()
