from flask import Flask
from views.common import common
app = Flask(__name__)

API = '/db/api'

app.register_blueprint(common, url_prefix=API)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
