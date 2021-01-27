from flask import Flask
from flask_rest3 import FlaskS3R


app = Flask(__name__)
s3r = FlaskS3R(url_prefix='/s3r')
s3r.init_app(app)

if __name__ == '__main__':
    app.run(debug=False)
