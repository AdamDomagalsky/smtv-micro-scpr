from pip._internal.req import parse_requirements
from setuptools import find_packages
from setuptools import setup


setup(
    name='smtv_api',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        str(ir.req) for ir in parse_requirements('base_requirements.txt', session=False)
    ],
    entry_points={
        'console_scripts': [
            'start_service = smtv_api.commands.start_service:run',
            'migrate = smtv_api.commands.migrate:run',
            'check_environment = smtv_api.commands.check_environment:run'
        ],
        'pytest11': [
            'environment = smtv_api.setup_test_environment',
        ],
    },
)
