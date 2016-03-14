from flask import Blueprint, request
from views.response_json import response

forum = Blueprint("forum", __name__)


# @forum.route("/create", methods=['POST'])
@forum.route("/create")
def create():
    # TODO
    return response(0, 'OK')


@forum.route("/details/", methods=['GET'])
# @forum.route("/details/")
def details():
    # TODO

    forum_name = request.args.get("forum")

    if forum_name:
        related = request.args.getlist('related')

        return response(0, 'good')
    else:
        return 'bad'


# @forum.route("/listThreads/", methods=['GET'])
@forum.route("/listThreads/")
def list_threads():
    # TODO

    forum_name = request.args.get("forum")

    if forum_name:
        since = request.args.get("since")
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        related = request.args.getlist('related')

        return response(0, 'good')
    else:
        return 'bad'


# @forum.route("/listUsers/", methods=['GET'])
@forum.route("/listUsers/")
def list_users():
    # TODO
    forum_name = request.args.get("forum")

    if forum_name:
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        since_id = request.args.getlist('since_id')

        return response(0, 'good')
    else:
        return 'bad'
