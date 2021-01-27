import json

from flask import Response
from flask import jsonify

from .schema import JSONSchema


class APIResponse(Response):
    default_mimetype = 'application/json'

    def __init__(self, data, code=200):
        if isinstance(data, JSONSchema):
            data = data.__dict__
        super().__init__(json.dumps(data), status=code, mimetype=self.default_mimetype)

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, JSONSchema):
            rv = jsonify(rv.json())
        return super(APIResponse, cls).force_type(rv, environ)
