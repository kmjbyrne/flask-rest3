# API

## Route Table

| Route                        | Purpose                                                             |
| ---------------------------- | ------------------------------------------------------------------- |
| GET: /                       | None                                                                |
| GET: /{bucket}               | S3 Bucket to query                                                  |
| GET: /{bucket}/{prefix}      | S3 prefixes are loosely analog to paths (although they don't exist) |
| GET: /{bucket}/{prefix}      | S3 prefixes are loosely analog to paths (although they don't exist) |
| GET: /{bucket}/{object-key}  | Returns a single object (if it is not a prefix)                     |
| HEAD: /{bucket}/{object-key} | Null content response -> (200 \| 404)                               |

## Additional Arguments

| Querystring Argument | Options                              | Purpose                                      |
| -------------------- | ------------------------------------ | -------------------------------------------- |
| recursive            | (true \| false) -> defaults to true  | Lists all objects under a prefix recursively |
| signature            | (true \| false) -> defaults to false | Returns a presigned URL for the object       |