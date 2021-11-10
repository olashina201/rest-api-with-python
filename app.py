from boto3.dynamodb.conditions import Key
import os
from chalice.app import Chalice
import boto3
from chalicelib import db
app = Chalice(app_name='rest-api-with-python')


def get_app_db():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table('blog')
    return table


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/blogs', methods=['GET'])
def list_blogs():
    response = get_app_db().scan()
    data = response.get('Items', None)
    return {'data': data}


@app.route('/post', methods=['POST'])
def create_post():
    data = app.current_request.json_body
    try:
        get_app_db().put_item(Item={
            "title": data['title'],
            "description": data['description'],
            "content": data['content']
        })
        return {'message': 'ok - CREATED', 'status': 201, 'data': data}
    except Exception as e:
        return {'message': str(e)}


@app.route('/blog/{id}', methods=['GET'])
def get_blog(id):
    response = get_app_db().query(
        KeyConditionExpression=Key("id").eq(id)
    )
    data = response.get('Items', None)
    return {'data': data}


@app.route('/blog/{id}', methods=['DELETE'])
def delete_blog(id):
    data = app.current_request.json_body
    try:
        response = get_app_db().delete_item(
            Key={
                "id": data['id'],
                "author": data['author']
            }
        )
        return {'message': 'ok - DELETED', 'status': 201}

    except Exception as e:
        return {'message': str(e)}
