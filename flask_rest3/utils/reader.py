from functools import wraps

import boto3

from botocore.exceptions import ClientError


# def head(cls):
#     def decorated(func):
#         def inner(self, bucket, key):
#             try:
#                 self.s3.head_object(Bucket=bucket, Key=key)
#             except ClientError:
#                 raise FileNotFoundError('This object does not exist in this bucket')
#         return decorated
#     return cls




class S3Reader:

    def __init__(self, bucket: str = None):
        self.bucket = bucket
        self.s3 = boto3.client('s3')
        """ :type : pyboto3.s3 """

    def head(func):
        @wraps(func)
        def decorated(self, **kwargs):
            try:
                if not kwargs.get('Key', None):
                    self.s3.head_bucket(Bucket=kwargs.get('Bucket'))
                    return func(self, **kwargs)
                self.s3.head_object(Bucket=kwargs.get('Bucket'), Key=kwargs.get('Key'))
            except ClientError:
                raise FileNotFoundError('This object does not exist in this bucket')
            return func(self, **kwargs)
        return decorated

    def generate_presigned_post(self, **kwargs):
        acl = None
        bucket = kwargs.get('Bucket') or self.bucket
        key = kwargs.get('Key')
        if kwargs.get('public'):
            acl = 'public-read'
        return self.s3.generate_presigned_post(Bucket=bucket, Key=key, Conditions=[dict(acl=acl)])

    @head
    def get_presigned_url(self, bucket, key, method='get_object'):
        bucket = bucket or self.bucket
        return self.s3.generate_presigned_url(
            ClientMethod=method,
            Params=dict(Bucket=bucket, Key=key)
        )

    @head
    def list_objects(self, *args, **kwargs):
        bucket = kwargs.get('Bucket', None)
        if not self.bucket and not bucket:
            raise ValueError('A bucket value must be provided or self on instantiation')
        objects = self.s3.list_objects(**kwargs)
        return objects


if __name__ == '__main__':
    S3Reader('amzui-cdn').list_objects()