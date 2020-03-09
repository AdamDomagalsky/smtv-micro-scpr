import datetime
import os

DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'
SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.environ.get('SERVER_PORT', default=80))
SQLALCHEMY_DATABASE_URI = os.environ['API_DATABASE_URL']

S3_ENDPOINT_URL = os.environ['S3_ENDPOINT_URL']
S3_BUCKET = os.environ['S3_BUCKET']
S3_ACCESS_KEY_ID = os.environ['S3_ACCESS_KEY_ID']
S3_SECRET_ACCESS_KEY = os.environ['S3_SECRET_ACCESS_KEY']

# CELERY
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
