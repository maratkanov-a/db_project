# -*- coding: utf-8 -*-
import json
from flask import Blueprint, request
from views.response_json import response

forum = Blueprint("forum", __name__)


# @forum.route("/create", methods=['POST'])
@forum.route("/create")
def create():

    params = json.loads(request.data)
    if params['name'] and params['short_name'] and params['user']:
        # TODO
        return response(0, 'OK')
    else:
        return 'bad'


@forum.route("/details/", methods=['GET'])
def details():

    forum_name = request.args.get("forum")

    if forum_name:
        related = request.args.getlist('related')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@forum.route("/listThreads/", methods=['GET'])
def list_threads():

    forum_name = request.args.get("forum")

    if forum_name:
        since = request.args.get("since")
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        related = request.args.getlist('related')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@forum.route("/listUsers/", methods=['GET'])
def list_users():

    forum_name = request.args.get("forum")

    if forum_name:
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        # TODO: [since_id,last_id]
        since_id = request.args.getlist('since_id')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'
