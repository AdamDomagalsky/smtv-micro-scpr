from typing import Dict, Any

import flask_restplus
from smtv_api import database


def _marshal_object(schema: flask_restplus.Model, obj: database.db.Model) -> Dict[str, Any]:
    result: Dict[str, Any] = flask_restplus.marshal_with(schema)(lambda o: o)(obj)

    return result
