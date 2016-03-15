import json
from flask import Blueprint, request
from response_json import response

thread = Blueprint("thread", __name__)


# @thread.route("/close", methods=['POST'])
@thread.route("/close")
def close():
    params = json.loads(request.data)

    if params['thread']:
        # TODO
        return response(0, 'OK')
    else:
        return 'bad'


# @thread.route("/create", methods=['POST'])
@thread.route("/create")
def create():
    params = json.loads(request.data)

    if params['forum'] and params['title'] and params['isClosed'] and params['user'] and params['date'] and params['message'] and params['slug']:
        # TODO
        return response(0, 'OK')
    else:
        return 'bad'


@thread.route("/details/", methods=['GET'])
def details():
    thread_id = request.args.get("thread", type=int)

    if thread_id:
        related = request.args.getlist('related')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@thread.route("/list/", methods=['GET'])
def list_threads():

    user_email = request.args.get("user")
    forum_name = request.args.get("forum")

    if user_email or forum_name:
        since = request.args.get("since", type=str)
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@thread.route("/listPosts/", methods=['GET'])
def list_posts_threads():

    thread_id = request.args.get("thread")

    if thread_id:
        since = request.args.get("since", type=str)
        limit = request.args.get("limit", type=int)
        sort = request.args.get("sort", type=str, default='flat')
        order = request.args.get("order", default='desc')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @thread.route("/open", methods=['POST'])
@thread.route("/open")
def open():

    params = json.loads(request.data)

    if params['thread']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @thread.route("/remove", methods=['POST'])
@thread.route("/remove")
def remove():

    params = json.loads(request.data)

    if params['thread']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @thread.route("/restore", methods=['POST'])
@thread.route("/restore")
def restore():

    params = json.loads(request.data)

    if params['thread']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @thread.route("/subscribe", methods=['POST'])
@thread.route("/subscribe")
def subscribe():

    params = json.loads(request.data)

    if params['thread'] and params['user']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @thread.route("/unsubscribe", methods=['POST'])
@thread.route("/unsubscribe")
def unsubscribe():

    params = json.loads(request.data)

    if params['thread'] and params['user']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @thread.route("/update", methods=['POST'])
@thread.route("/update")
def update():
    params = json.loads(request.data)

    if params['message'] and params['slug'] and params['thread']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @thread.route("/vote", methods=['POST'])
@thread.route("/vote")
def vote():
    params = json.loads(request.data)

    if params['thread'] and params['vote']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'
