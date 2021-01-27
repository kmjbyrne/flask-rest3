# Flask-S3R

Flask-S3R is a pre-baked, simple-to-use Flask extension that allows you to work seamlessly with AWS S3 buckets by use of
a REST JSON API. The inspiration behind this extension was DRY frustration with writing boilerplate code for projects that
uses S3 buckets and simply operation like generate presigned URLs for POST requests.

Hooking up to SPAs or other frontends allows you effectively use S3 as a filesystem with a secure upload process. As all
permissions are still handled by IAM, it effectively decouples your application from too many concerns around unauthorised
uploads and access.

For development, the API integrates with your AWS account using the normal credentials (read from the shared credentials 
local config) and integrates well with the recommended app factory pattern. This way, you can set dev, test, production
buckets with just a few lines in your app config.

> Flask-S3R will ignore route relative errors by default. See Configuration section for how to enable.

## Examples

### Basic Application

```python
from flask import Flask

from flask_rest3 import FlaskS3R

app = Flask(__name__)
s3r = FlaskS3R()

if __name__ == '__main__':
    s3r.init_app(app)
    app.run(debug=True)
```

#### Query

Then query your bucket:

```bash
curl localhost:5000/s3r/{bucket-name}
```


```bash
curl localhost:5000/s3r/{bucket-name}/{object-key}
```

#### Query Recursive

To query a bucket and get all results using a recursive operation, simply call with the recursive querystring parameter.

Like so:

```bash
curl localhost:5000/s3r/{bucket-name}?recursive=true
```

### Using Application Config

```python
from flask import Flask

from flask_rest3 import FlaskS3R

s3r = FlaskS3R()


class Config:
    pass


class Develop(Config):
    S3R_BUCKET = 'your-dev-bucket-name'


class Testing(Config):
    S3R_BUCKET = 'your-test-bucket-name'


def app_factory(env='DEV'):
    app = Flask(__name__)

    conf = Develop
    if env == 'TEST':
        conf = Testing

    s3r.init_app(app)
    app.config.from_object(conf)
    return app


if __name__ == '__main__':
    app.run(debug=True)
```





