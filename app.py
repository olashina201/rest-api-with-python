from chalice.app import Chalice

app = Chalice(app_name='rest-api-with-python')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/post', methods=['POST'])
def create_post():
    request = app.current_request
    message = request.json_body
    return message
