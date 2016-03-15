import json
from flask import Blueprint, request
from views.response_json import response

post = Blueprint("post", __name__)


# @post.route("/create", methods=['POST'])
@post.route("/create")
def create():

    params = json.loads(request.data)
    if params['date'] and params['thread'] and params['message'] and params['user'] and params['forum']:
        # TODO
        return response(0, 'OK')
    else:
        return 'bad'


@post.route("/details/", methods=['GET'])
def details():

    post_id = request.args.get("post", type=int)

    if post_id:
        related = request.args.getlist('related')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@post.route("/list/", methods=['GET'])
def list_posts():
    # TODO

    forum_name = request.args.get("forum")
    thread_id = request.args.get("thread")

    if forum_name or thread_id:
        since = request.args.get("since", type=str)
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')

        return response(0, 'good')
    else:
        return 'bad'


# @post.route("/remove", methods=['POST'])
@post.route("/remove")
def remove():

    params = json.loads(request.data)

    if params['post']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @post.route("/restore", methods=['POST'])
@post.route("/restore")
def restore():

    params = json.loads(request.data)

    if params['post']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @post.route("/update", methods=['POST'])
@post.route("/update")
def update():

    params = json.loads(request.data)

    if params['post'] and params['message']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @post.route("/vote", methods=['POST'])
@post.route("/vote")
def vote():

    params = json.loads(request.data)

    if params['post'] and params['vote']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'
