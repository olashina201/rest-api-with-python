import os
from chalice.app import Chalice, AuthResponse
import boto3
from chalicelib import  db
app = Chalice(app_name='rest-api-with-python')
app.debug = True
_DB = None


def get_app_db():
    global _DB
    if _DB is None:
        _DB = db.DynamoDBBlog(
            boto3.resource('dynamodb').Table(
                os.environ['APP_TABLE_NAME'])
        )
    return _DB

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/blogs', methods=['GET'])
def list_blogs():
    return get_app_db().list_items()


@app.route('/post', methods=['POST'])
def create_post():
    request = app.current_request
    message = request.json_body
    return message
