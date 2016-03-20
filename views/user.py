import json
import MySQLdb
from flask import Blueprint, request
from views.response_json import response, connection, dictfetchall, true_or_false, fix_user_dict, fix_post_dict


def list_posts(cursor):
    posts_list = []
    for one_el in cursor.fetchall():
        posts_dict = {
            'data': str(one_el[4]),
            'dislikes': one_el[6],
            'forum': one_el[1],
            'id': one_el[0],
            'isApproved': true_or_false(one_el[12]),
            'isDeleted': true_or_false(one_el[15]),
            'isEdited': true_or_false(one_el[14]),
            'isHighlighted': true_or_false(one_el[11]),
            'isSpam': true_or_false(one_el[13]),
            'likes': one_el[7],
            'message': one_el[5],
            'parent': one_el[9],
            'points': one_el[8],
            'thread': one_el[1],
            'user': one_el[2]
        }
        posts_list.append(posts_dict)
    return posts_list

user = Blueprint("user", __name__)


@user.route("/create", methods=['POST'])
def create():

    params = json.loads(request.data)

    if params['username'] and params['about'] and params['name'] and params['email']:
        if not params['isAnonymous']:
            params['isAnonymous'] = 0
            is_anonymous = False
        else:
            params['isAnonymous'] = 1
            is_anonymous = True

        c, conn = connection()
        try:
            c.execute(
                '''insert into `User` (`username`, `about`, `email`, `name`, `isAnonymous`) values ('{}','{}','{}','{}','{}') '''.format(
                    params['username'], params['about'], params['email'], params['name'], params['isAnonymous']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(5, 'User already exists')

        response_dict = {
            'username': params['username'],
            'about': params['about'],
            'name': params['name'],
            'email': params['email'],
            'isAnonymous': is_anonymous
        }

        conn.close()

        return response(0, response_dict)
    else:
        return response(2, 'Invalid request')


@user.route("/details/", methods=['GET'])
def details():
    user_email = request.args.get("user", type=str, default=None)

    if user_email:

        c, conn = connection()
        try:
            c.execute(''' select * from User u where u.email = '{}' '''.format(user_email))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        users_tuple = c.fetchall()

        res = fix_user_dict(c, users_tuple[0])

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/follow", methods=['POST'])
def follow():

    params = json.loads(request.data)

    if params['follower'] and params['followee']:

        c, conn = connection()
        try:
            c.execute('''insert into `Follow` (`follower`, `followee`) values ('{}','{}') '''.format(params['follower'],
                                                                                                 params['followee']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        try:
            c.execute(''' select * from User u where u.email = '{}' '''.format(params['follower']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/listFollowers/", methods=['GET'])
def list_followers():

    user_email = request.args.get("user", type=str, default=None)

    if user_email:

        limit = request.args.get("limit", type=int, default=None)

        if limit:
            limit_str = 'limit {}'.format(limit)
        else:
            limit_str = ''

        order = request.args.get("order", default='desc')

        if order not in ['asc', 'desc']:
            return response(3, 'Wrong order value')

        since_id = request.args.get('since_id', type=str, default=None)

        if since_id:
            since_id_list = map(int, since_id.rstrip(']').lstrip('[').split(','))
            since_id_str = ''' and u.id >= '{}' and u.id <= '{}' '''.format(since_id_list[0], since_id_list[1])
        else:
            since_id_str = ''

        c, conn = connection()

        try:
            c.execute(''' select * from Follow f join User u on f.follower = u.email where f.followee='{}' {} order by u.name {} {} '''.format(user_email, since_id_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = dictfetchall(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/listFollowing/", methods=['GET'])
def list_following():

    user_email = request.args.get("user", type=str, default=None)

    if user_email:

        limit = request.args.get("limit", type=int, default=None)

        if limit:
            limit_str = 'limit {}'.format(limit)
        else:
            limit_str = ''

        order = request.args.get("order", default='desc')

        if order not in ['asc', 'desc']:
            return response(3, 'Wrong order value')

        since_id = request.args.get('since_id', type=str, default=None)

        if since_id:
            since_id_list = map(int, since_id.rstrip(']').lstrip('[').split(','))
            since_id_str = ''' and u.id >= '{}' and u.id <= '{}' '''.format(since_id_list[0], since_id_list[1])
        else:
            since_id_str = ''

        c, conn = connection()

        try:
            c.execute(''' select * from Follow f join User u on f.followee = u.email where f.follower='{}' {} order by u.name {} {} '''.format(user_email, since_id_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = dictfetchall(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/listPosts/", methods=['GET'])
def list_posts_users():
    user_email = request.args.get("user", type=str)

    if user_email:

        since = request.args.get("since", type=str, default='1981-01-01 00:00:00')

        limit = request.args.get("limit", type=int, default=None)

        if limit:
            limit_str = 'limit {}'.format(limit)
        else:
            limit_str = ''

        order = request.args.get("order", default='desc')

        if order not in ['asc', 'desc']:
            return response(3, 'Wrong order value')

        c, conn = connection()

        try:
            c.execute(''' select * from Post p where p.user = '{}' and p.date > '{}' order by p.date {} {} '''.format(user_email, since, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_post_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/unfollow", methods=['POST'])
def unfollow():

    params = json.loads(request.data)

    if params['follower'] and params['followee']:

        c, conn = connection()

        try:
            c.execute(''' delete from Follow where follower='{}' and followee='{}' '''.format(params['follower'], params['followee']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')
        try:
            c.execute(''' select * from User u where u.email = '{}' '''.format(params['follower']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/updateProfile", methods=['POST'])
def update_user():

    params = json.loads(request.data)

    if params['about'] and params['user'] and params['name']:

        c, conn = connection()

        try:
            c.execute(''' update User u set name='{}', about='{}' where u.email='{}' '''.format(params['name'], params['about'], params['user']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')
        try:
            c.execute(''' select * from User u where u.email = '{}' '''.format(params['user']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')
