:tocdepth: 2

Flask Rest3
===========

Hello! Welcome to Flask Rest3 documentation!

Flask-S3R is a pre-baked, simple-to-use Flask extension that allows you to work seamlessly with AWS S3 buckets by use of
a REST JSON API. The inspiration behind this extension was DRY frustration with writing boilerplate code for projects that
use S3 buckets and simple operations like searching and generate presigned URLs for POST requests.

Hooking up to SPAs or other frontends allows you effectively use S3 as a filesystem with a secure upload process. As all
permissions are still handled by IAM, it effectively decouples your application from too many concerns around unauthorised
uploads and access.

For development, the API integrates with your AWS account using the normal credentials (read from the shared credentials
local config) and integrates well with the recommended app factory pattern. This way, you can set dev, test, production
buckets with just a few lines in your app config.

.. toctree::
    :maxdepth: 2

    quickstart.md


API Reference
-------------

If you are looking for information on a specific function, class or
method, this part of the documentation is for you.
