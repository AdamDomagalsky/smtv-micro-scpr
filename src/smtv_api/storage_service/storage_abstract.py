import http
import json
import re
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Tuple
from urllib.parse import urlparse

from smtv_api import schemas
from smtv_api.helpers import helpers


class StorageServiceABC(ABC):

    @staticmethod
    @abstractmethod
    def cut_prefix(base_str: str) -> str:
        return re.sub(
            re.compile('^(s3:|)(.+)', re.IGNORECASE),
            r'\3',
            base_str
        )

    @staticmethod
    @abstractmethod
    def validate_file(file_name: str) -> None:
        with open(file_name) as file:
            for line in file.readlines():
                try:
                    helpers.validate_payload(json.loads(line), schemas.RECORD)
                except json.JSONDecodeError:
                    helpers.error_abort(
                        http.HTTPStatus.UNPROCESSABLE_ENTITY,
                        'Given ndjson decode error - make sure that each line of your input file is in json format'
                    )

    @staticmethod
    @abstractmethod
    def get_params(url_to_parse: str) -> Tuple[str, str]:
        parsed_url = urlparse(url_to_parse)
        return parsed_url.netloc, parsed_url.path.lstrip('/')

    @abstractmethod
    def get_object_url(cls, object_name: str, root_name: str) -> str:
        raise NotImplementedError
