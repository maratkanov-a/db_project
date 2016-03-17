from flask import Flask
from views.common import common
from views.forum import forum
from views.post import post
from views.thread import thread
from views.user import user

app = Flask(__name__)

API = '/db/api'

app.register_blueprint(common, url_prefix=API)
app.register_blueprint(forum, url_prefix=API+'/forum')
app.register_blueprint(post, url_prefix=API+'/post')
app.register_blueprint(user, url_prefix=API+'/user')
app.register_blueprint(thread, url_prefix=API+'/thread')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
