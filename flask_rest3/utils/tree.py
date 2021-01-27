from datetime import datetime
from flask import request


def object_parser(obj: dict):
    """
    Turns S3 response objects into normalised dictionary objects
    :param obj:
    :return:
    """

    return dict(
        key=obj.get('Key'),
        modified=obj.get('LastModified').isoformat(),
        size=obj.get('Size')
    )


def object_list_to_tree(objects: [], bucket, bucket_meta):
    tree = {}
    nodes = {0: tree}

    for obj in objects or []:
        key = obj.get('Key')
        paths = key.split('/')
        for (idx, branch) in enumerate(paths):
            if branch == '':
                continue

            if not nodes.get(branch, None):
                nodes[branch] = {}

                if idx == len(paths) - 1:
                    nodes[branch] = object_parser(obj)
                    nodes[branch]['self'] = f'{request.base_url}/{key}'
                    url = 'https://{0}.{2}.amazonaws.com/{1}'.format(bucket, key, bucket_meta.get('LocationConstraint'))
                    nodes[branch]['url'] = url

            if idx > 0:
                nodes[paths[idx - 1]][branch] = nodes[branch]
            else:
                nodes[0][branch] = nodes[branch]
    return nodes[0]
