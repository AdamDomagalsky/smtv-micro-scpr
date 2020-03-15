import functools
import http
import logging
import typing

import flask_restplus
from smtv_api import database
from flask import request, make_response, jsonify

logger = logging.getLogger(__name__)


def get_payload(api_model: flask_restplus.Model) -> typing.Dict[str, typing.Any]:
    if (not request.is_json):
        error_abort(http.HTTPStatus.BAD_REQUEST, f'API endpoint expect application/json content-type')

    payload = request.get_json()

    return translate_keys(api_model, payload)


def translate_keys(api_model: flask_restplus.Model, data: dict) -> dict:
    """
    Recursive function helper for translating each payload key to `attribute` defined in `__init__` of the `Field`
    and cleaning unwanted keys that are not declared in model
    """
    diff: dict = api_model.keys() - data.keys()
    default_key_values: dict = {}
    for key in diff:
        field = api_model[key] if key in api_model else None
        if field.default:
            default_key_values[key] = field.default

    cleaned_data = {key: value for key, value in data.items() if key in api_model}
    cleaned_data = {**cleaned_data, **default_key_values}
    translated = {}
    for key, value in cleaned_data.items():
        field = api_model[key] if key in api_model else None
        key = api_model[key].attribute or key
        if isinstance(field, flask_restplus.fields.Nested):
            model: flask_restplus.Model = field.model
            value = translate_keys(model, value)
            translated[key] = value
        elif isinstance(field, flask_restplus.fields.List):
            items = []
            for item in value:
                if isinstance(field.container, flask_restplus.fields.Nested):
                    translated_item = translate_keys(field.container.model, item)
                    items.append(translated_item)
                else:
                    items.append(item)
            translated[key] = items
        else:
            translated[key] = value
    return translated


def validate_payload(
        payload: typing.Dict[str, typing.Any],
        api_model: flask_restplus.Model,
        ith_line: typing.Any = None) -> None:
    for key in api_model:
        # check if any reqd fields are missing in payload
        if key not in payload and api_model[key].required:
            if ith_line:
                error_abort(
                    http.HTTPStatus.UNPROCESSABLE_ENTITY,
                    f'Required field \'{key}\' missing, check line no. {ith_line}'
                )
            else:
                error_abort(http.HTTPStatus.UNPROCESSABLE_ENTITY, f'{api_model.name} required field \'{key}\' missing')

    # check payload
    for key in payload:
        field = api_model[key] if key in api_model else None
        if isinstance(field, flask_restplus.fields.List):
            field = field.container
            data = payload[key]
        else:
            data = [payload[key]]

        # check if string is not empty
        if isinstance(field, flask_restplus.fields.String):
            for stringValue in data:
                if not stringValue:
                    if ith_line:
                        error_abort(
                            http.HTTPStatus.UNPROCESSABLE_ENTITY,
                            f'Required field \'{key}\' has an empty value, check line no. {ith_line}'
                        )
                    else:
                        error_abort(
                            http.HTTPStatus.UNPROCESSABLE_ENTITY,
                            f'Required field \'{key}\' has an empty value'
                        )


def error_abort(code: http.HTTPStatus, message: str) -> None:
    """
    Abstraction over restplus `abort`.
    Returns error with the status code and message.
    """
    error = {
        'code': code,
        'message': message
    }
    flask_restplus.abort(code, error=error)


