import json
from flask import Blueprint, request
from views.response_json import response

user = Blueprint("user", __name__)


# @user.route("/create", methods=['POST'])
@user.route("/create")
def create():

    params = json.loads(request.data)

    if params['username'] and params['about'] and params['name'] and params['email']:
        # TODO
        return response(0, 'OK')
    else:
        return 'bad'


@user.route("/details/", methods=['GET'])
def details():

    user_email = request.args.get("email", type=str)

    if user_email:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @user.route("/follow", methods=['POST'])
@user.route('/follow')
def follow():

    params = json.loads(request.data)

    if params['follower'] or params['followee']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@user.route("/listFollowers/", methods=['GET'])
def list_followers():

    user_email = request.args.get("user", type=str)

    if user_email:
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        # TODO: границы
        since_id = request.args.getlist('since_id')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@user.route("/listFollowing/", methods=['GET'])
def list_following():

    user_email = request.args.get("user", type=str)

    if user_email:
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        # TODO: границы
        since_id = request.args.getlist('since_id')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


@user.route("/listPosts/", methods=['GET'])
def list_posts():

    user_email = request.args.get("user", type=str)

    if user_email:
        since = request.args.get("since", type=str)
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @user.route("/unfollow", methods=['POST'])
@user.route("/unfollow")
def update():

    params = json.loads(request.data)

    if params['follower'] or params['followee']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'


# @user.route("/updateProfile", methods=['POST'])
@user.route("/updateProfile")
def update():

    params = json.loads(request.data)

    if params['about'] and params['user'] and params['name']:
        # TODO
        return response(0, 'good')
    else:
        return 'bad'
