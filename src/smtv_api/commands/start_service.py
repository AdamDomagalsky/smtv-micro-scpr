import os

from smtv_api import settings
from smtv_api import flask_app


def run() -> None:
    if settings.DEBUG:
        flask_app.create_web_app().run(host=settings.SERVER_HOST, port=settings.SERVER_PORT)
    else:
        os.execv('/usr/local/bin/uwsgi', [
            'uwsgi',
            '--http', f'{settings.SERVER_HOST}:{settings.SERVER_PORT}',
            '--ini', 'uwsgi.ini',
        ])


if __name__ == '__main__':
    run()
