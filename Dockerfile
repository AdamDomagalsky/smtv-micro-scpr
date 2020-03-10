FROM python:3.7.2 as smtv-api

WORKDIR /srv

RUN pip install \
    flake8==3.6.0 \
    pip-tools==3.3.1 \
    mypy==0.650

RUN chgrp -R root /usr/local
COPY requirements.txt /srv/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src /srv
COPY wait-for-it.sh /wait-for-it.sh
RUN pip install --no-deps --editable .
# enable usage of console_scripts declared in setup.py
RUN mv smtv_api.egg-info /usr/local/lib/python3.7/site-packages

CMD ["start_service"]

# Celery worker
FROM smtv-api as smtv-worker-celery

COPY celery-requirements.txt /srv/celery-requirements.txt
RUN pip install -r celery-requirements.txt

ENTRYPOINT [ "celery" ]
CMD [ "-A tasks worker" ]