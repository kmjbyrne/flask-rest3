# Explore

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

``` important:: 
    This is a rather privileged example and you shouldn't expose your buckets like this. 
    Please make sure that the run user has only limited access to buckets while you develop or test your applications.
```

Then query your API for bucket contents:

``curl localhost:5000/s3r/{bucket-name}``


``curl localhost:5000/s3r/{bucket-name}/{object-key}``

Query Recursive

To query a bucket and get all results using a recursive operation, simply call with the recursive querystring parameter.

Like so:

``curl localhost:5000/s3r/{bucket-name}?recursive=true``

### Using Application Config

To use Rest3 with the application factory pattern, one can designate buckets per environment, this way, the URL with
assigned prefix will fallback to the bucket for that configuration.

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

And the query would look like the following:

`curl localhost:5000/s3r`

``` note::
    The bucket parameter is not required when using the environment config like this.
```


# Endpoints

## Route Table

| Route                        | Purpose                                                             |
| ---------------------------- | ------------------------------------------------------------------- |
| GET: /                       | None                                                                |
| GET: /{bucket}               | S3 Bucket to query                                                  |
| GET: /{bucket}/{prefix}      | S3 prefixes are loosely analog to paths (although they don't exist) |
| GET: /{bucket}/{prefix}      | S3 prefixes are loosely analog to paths (although they don't exist) |
| GET: /{bucket}/{object-key}  | Returns a single object (if it is not a prefix)                     |
| HEAD: /{bucket}/{object-key} | Null content response -> (200 \| 404)                               |
| POST: /{bucket}/{object-key}  | Returns a resource token for creating new objects in a bucket                  |

### Additional Arguments

| Querystring Argument | Options                              | Purpose                                      |
| -------------------- | ------------------------------------ | -------------------------------------------- |
| recursive            | (true \| false) -> defaults to true  | Lists all objects under a prefix recursively |
| signature            | (true \| false) -> defaults to false | Returns a presigned URL for the object       |



## Creating Objects

Boto3 allows for the objects to be uploaded safely by using presigned URLs. S3R exposes an endpoint that provides your
client will the required temporary tokens to do so.

Using the POST method from the route table, we can effectively create a token that can be used by any client without 
needed to have AWS SDKs installed. It works by using a basic HTTP request with the object as FormData for the request, 
and the token serves as a grant to perform the action but ***only*** on that object. 

### Usage

```curl localhost:5000/{bucket}/{object-key}```

If the object doesn't already exist in the bucket, the response will be similar to:

```json
{
    "links": {
        "self": "http://localhost:5000/s3r/{BUCKET}/{OBJECT}"
    },
    "data": {
        "url": "https://{BUCKET}.s3.amazonaws.com/",
        "fields": {
            "key": "{OBJECT}",
            "AWSAccessKeyId": "XXXX",
            "policy": "XXXX",
            "signature": "XXXX"
        }
    }
}
```

Here is an example of a TypeScript/Pseudocode function that marshals the data and creates a request for an HTTP client to run:

```typescript
makeRequest(signature: any, file: File, filename: string): FormData {
    const formData = new FormData();
    Object.entries(signature.fields).forEach(([k, v]) => {
        formData.append(k, v.toString());
    });
    formData.append('file', file, filename);
    return formData;
}

...
Assume we have already gotten our response from the Flask API
...

const file; // File will be local to the browser or client
upload(signature: any) {
    const s3Filename = signature.key;
    const formData = makeRequest(signature, file, s3Filename)
    
    http(signature.url, formData)
}
```

This allows any client that uses the fields in this response to upload an object that matches the filename for this
signature. Once the request has been made, S3 will return an empty response that confirms the multi-part upload was
successful.

## Access Control Lists


To limit the number of buckets that the application even attempts connection to (ideally in addition to IAM policies),
you can leverage the app config again and designate buckets that are access permitted by using ALLOW/DENY ACLs like so:

```python
class Develop:
    # if using ALLOW only, only the buckets bucket-name-a and bucket-name-b will be permitted
    S3R_ALLOW = ('bucket-name-a', 'bucket-name-b')

    ...
    # if using DENY only, all buckets except bucket-name-c will be permitted
    S3R_DENY = ('bucket-name-c')
```
    

