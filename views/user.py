# -*- coding: utf-8 -*-
import json
import MySQLdb
from flask import Blueprint, request
from views.response_json import *


user = Blueprint("user", __name__)


@user.route("/create/", methods=['POST'])
def create():

    params = json.loads(request.data)

    if (params['username'] and params['about'] and params['name'] and params['email']) or params['isAnonymous']:

        if not params['isAnonymous']:
            params['isAnonymous'] = 0
        else:
            params['isAnonymous'] = 1
            params['username'] = ''
            params['about'] = ''
            params['name'] = ''

        c, conn = connection()
        try:
            c.execute(
                '''insert into `User` (`username`, `about`, `email`, `name`, `isAnonymous`) values ('{}','{}','{}','{}','{}') '''.format(
                    params['username'], params['about'], params['email'], params['name'], params['isAnonymous']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(5, 'User already exists')

        try:
            c.execute(
                ''' select * from User u where u.email='{}' '''.format(params['email']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not found')

        if c.rowcount == 0:
            return response(1, 'Not Found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res[0])
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

        if c.rowcount == 0:
            return response(1, 'Not Found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@user.route("/follow/", methods=['POST'])
def follow():

    params = json.loads(request.data)

    if params['follower'] and params['followee']:

        c, conn = connection()
        try:
            c.execute('''insert into `Follow` (`follower`, `followee`) values ('{}','{}') '''.format(params['follower'],
                                                                                                 params['followee']))
            conn.commit()
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

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@user.route("/listFollowers/", methods=['GET'])
def list_followers():

    user_email = request.args.get("user", type=str, default=None)

    if user_email:

        limit = request.args.get("limit", type=int, default=None)

        order = request.args.get("order", default='desc')

        limit_str = check_limit(limit)

        if order not in ['asc', 'desc']:
            return response(3, 'Wrong order value')

        since_id = request.args.get('since_id', type=str, default=None)

        if since_id:
            since_id_str = ''' and u.id >= '{}' '''.format(since_id)
        else:
            since_id_str = ''

        c, conn = connection()

        try:
            c.execute(''' select * from Follow f join User u on f.follower = u.email where f.followee='{}' and u.id {} order by u.name {} {} '''.format(user_email, since_id_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/listFollowing/", methods=['GET'])
def list_following():

    user_email = request.args.get("user", type=str, default=None)

    if user_email:

        limit = request.args.get("limit", type=int, default=None)

        limit_str = check_limit(limit)

        order = request.args.get("order", default='desc')

        if order not in ['asc', 'desc']:
            return response(3, 'Wrong order value')

        since_id = request.args.get('since_id', type=str, default=None)

        if since_id:
            since_id_str = ''' and u.id >= '{}' '''.format(since_id)
        else:
            since_id_str = ''

        c, conn = connection()

        try:
            c.execute(''' select * from Follow f join User u on f.followee = u.email where f.follower='{}' and u.id {} order by u.name {} {} '''.format(user_email, since_id_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/listPosts/", methods=['GET'])
def list_posts_users():
    user_email = request.args.get("user", type=str)

    if user_email:

        since = request.args.get("since", type=str, default=None)

        limit = request.args.get("limit", type=int, default=None)

        limit_str = check_limit(limit)

        since_str = check_since(since)

        order = request.args.get("order", default='desc')

        if order not in ['asc', 'desc']:
            return response(3, 'Wrong order value')

        c, conn = connection()

        try:
            c.execute(''' select * from Post p where p.user = '{}' {} order by p.date {} {} '''.format(user_email, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_post_dict(c, [])

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@user.route("/unfollow/", methods=['POST'])
def unfollow():

    params = json.loads(request.data)

    if params['follower'] and params['followee']:

        c, conn = connection()

        try:
            c.execute(''' delete from Follow where follower='{}' and followee='{}' '''.format(params['follower'], params['followee']))
            conn.commit()
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

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@user.route("/updateProfile/", methods=['POST'])
def update_user():

    params = json.loads(request.data)

    if params['about'] and params['user'] and params['name']:

        c, conn = connection()

        try:
            c.execute(''' update User u set name='{}', about='{}' where u.email='{}' '''.format(params['name'], params['about'], params['user']))
            conn.commit()
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

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')
