import boto3

from flask import Flask
from flask import request
from flask import Blueprint
from flask import abort

from .utils.reader import S3Reader
from .utils.tree import object_list_to_tree
from .utils.tree import object_parser
from .utils.schema import JSONSchema
from .utils.response import APIResponse


s3r = Blueprint('flask-s3r', __name__)
s3 = S3Reader()


class FlaskS3R:
    def __init__(self, app=None, url_prefix='s3r'):
        self.app = app
        self.url_prefix = url_prefix

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        app.config.setdefault('S3R_ERRORS', True)
        app.config.setdefault('S3R_URL_PREFIX', self.url_prefix)

        if app.config.get('S3R_ERRORS'):
            @s3r.app_errorhandler(Exception)
            @s3r.app_errorhandler(FileNotFoundError)
            @s3r.app_errorhandler(404)
            def errorhandler(error):
                resp = APIResponse(dict(error=str(error)), code=getattr(error, 'code', 500))
                return resp

        app.register_blueprint(s3r, url_prefix=self.url_prefix)


def s3_call(bucket, key=None):
    # z = S3Reader().s3.list_objects(Bucket=bucket, Prefix='', Delimiter='/')
    query = dict(request.args)
    bucket_metadata = boto3.client('s3').get_bucket_location(Bucket=bucket)

    contents = s3.s3.list_objects(Bucket=bucket, Prefix=key or '', Delimiter='/')

    files = [object_parser(f) for f in contents.get('Contents', list())]
    folders = [dict(key=f.get('Prefix'), type='path') for f in contents.get('CommonPrefixes', list())]

    if not files and not folders:
        raise abort(404, 'This path prefix of object key does not exist.')

    if query.get('recursive', False) or query.get('r', False):
        objects = s3.s3.list_objects(Bucket=bucket, Prefix=key or '', Delimiter='')
        return object_list_to_tree(objects.get('Contents'), bucket, bucket_metadata)

    files.extend(folders)
    return files


@s3r.route('<bucket>/<path:path>', methods=['POST'])
def post_object_signature(bucket: str, path: str):
    url = S3Reader(bucket).generate_presigned_post(Bucket=bucket, Key=path)
    resp = JSONSchema()
    resp.links['self'] = request.url
    resp.data = url
    return APIResponse(resp)


@s3r.route('/<bucket>', methods=['GET'])
@s3r.route('/<bucket>/<path:path>', methods=['GET'])
def get_object(bucket: str, path: str = None):
    tree = s3_call(bucket, path)
    resp = JSONSchema()
    resp.links['self'] = request.url
    resp.data = tree
    return APIResponse(resp)
