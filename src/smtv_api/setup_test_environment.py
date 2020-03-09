import os


def pytest_configure(config: dict) -> None:
    setup()


def setup() -> None:
    os.environ['AIRFLOW_API_ROOT_URL'] = 'http://test-airflow/api/experimental/'
    os.environ['API_DATABASE_URL'] = 'postgres://postgres:postgres@postgres:5432/postgres'

    os.environ['S3_ENDPOINT_URL'] = 'http://localhost:5000/'
    os.environ['S3_BUCKET'] = 'test-bucket'

    os.environ['S3_ACCESS_KEY_ID'] = 'inner-access-key'
    os.environ['S3_SECRET_ACCESS_KEY'] = 'inner-secret-access-key'

    os.environ['CELERY_BROKER_URL'] = 'pyamqp://rabbitmq:rabbitmq@rabbit:5672//'
    os.environ['CELERY_RESULT_BACKEND'] = 'rpc://'
