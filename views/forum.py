# -*- coding: utf-8 -*-
import json
import MySQLdb
from flask import Blueprint, request
from views.response_json import *

forum = Blueprint("forum", __name__)


@forum.route("/create", methods=['POST'])
def create():

    params = json.loads(request.data)

    if params['name'] and params['short_name'] and params['user']:

        c, conn = connection()

        try:
            c.execute(
                '''insert into `Forum` (`name`, `short_name`, `user`) values ('{}','{}','{}') '''.format(
                    params['name'], params['short_name'], params['user']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        try:
            c.execute(
                '''select * from Forum f where f.name='{}' and f.short_name='{}' and f.user='{}' limit 1 '''.format(
                    params['name'], params['short_name'], params['user']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not found')

        res = dictfetchall(c)

        conn.close()

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@forum.route("/details/", methods=['GET'])
def details():

    forum_name = request.args.get("forum", type=str, default=None)
    related = request.args.getlist('related', type=str)

    if forum_name:

        c, conn = connection()

        try:
            c.execute(
                '''select * from Forum f where f.short_name='{}' '''.format(forum_name))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not found')

        res = fix_forum_dict(c, related)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@forum.route("/listPosts/", methods=['GET'])
def list_posts():

    forum_name = request.args.get("forum", type=str, default=None)
    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')
    related = request.args.getlist('related', type=str)

    if order not in ['asc', 'desc']:
        return response(3, 'Wrong order value')

    limit_str = check_limit(limit)

    since_str = check_since(since)

    if forum_name:

        c, conn = connection()

        try:
            c.execute(
                '''select * from Post p where p.forum='{}' {} order by p.date {} {} '''.format(forum_name, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not found')

        res = fix_post_dict(c, related)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@forum.route("/listThreads/", methods=['GET'])
def list_threads():

    forum_name = request.args.get("forum", type=str, default=None)
    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')
    related = request.args.getlist('related', type=str)

    if order not in ['asc', 'desc']:
        return response(3, 'Wrong order value')

    limit_str = check_limit(limit)

    since_str = check_since(since)

    if forum_name:

        c, conn = connection()

        try:
            c.execute(
                '''select * from Thread t where t.forum='{}' {} order by t.date {} {} '''.format(forum_name, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not found')

        res = fix_thread_dict(c, related)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@forum.route("/listUsers/", methods=['GET'])
def list_users():

    forum_name = request.args.get("forum", type=str, default=None)

    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')
    since_id = request.args.get('since_id', type=str, default=None)

    if since_id:
        since_id_list = map(int, since_id.rstrip(']').lstrip('[').split(','))
        since_id_str = ''' u.id >= '{}' and u.id <= '{}' and '''.format(since_id_list[0], since_id_list[1])
    else:
        since_id_str = ''

    if order not in ['asc', 'desc']:
        return response(3, 'Wrong order value')

    limit_str = check_limit(limit)

    if forum_name:

        c, conn = connection()

        try:
            c.execute(
                '''select * from User u where {} u.email in ( select distinct p.user from Post p where p.forum='{}' ) order by u.name {} {} '''.format(since_id_str, forum_name, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not found')

        res = fix_user_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')
