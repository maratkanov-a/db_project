# -*- coding: utf-8 -*-
import json
import MySQLdb
from flask import Blueprint, request
from response_json import *

thread = Blueprint("thread", __name__)


@thread.route("/close/", methods=['POST'])
def close():

    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()
        try:
            c.execute(''' update Thread t set isClosed=1 where t.id={} '''.format(params['thread']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/create/", methods=['POST'])
def create():

    params = json.loads(request.data)

    if params['forum'] and params['title'] and str(params['isClosed']) and params['user'] and params['date'] and params[
        'message'] and params['slug']:

        if not params.get('isDeleted', None):
            params['isDeleted'] = 0
        else:
            params['isDeleted'] = 1

        if params.get('isClosed', None):
            is_closed = 1
        else:
            is_closed = 0

        c, conn = connection()
        try:
            c.execute(
            '''insert into `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`, `isDeleted`, `isClosed`) values ('{}', '{}','{}','{}','{}','{}','{}','{}') '''.format(
                params['forum'], params['title'].encode("utf8"), params['user'], params['date'], params['message'].encode("utf8"), params['slug'].encode("utf8"), params['isDeleted'],
                is_closed))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        try:
            c.execute(''' select * from Thread t where t.date='{}' '''.format(params['date']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_thread_dict(c, [])[0]

        res.pop("likes", None)
        res.pop("dislikes", None)
        res.pop("points", None)
        res.pop("posts", None)

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/details/", methods=['GET'])
def details():

    thread_id = request.args.get("thread", type=int, default=None)
    related = request.args.getlist('related', type=str)

    if len([item for item in related if item not in ['user', 'forum']]) > 0:
        return response(3, "Incorrect request")

    if thread_id:

        c, conn = connection()
        try:
            c.execute(''' select * from Thread t where t.id='{}' '''.format(thread_id))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_thread_dict(c, related)

        conn.close()

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@thread.route("/list/", methods=['GET'])
def list_threads():

    user_email = request.args.get("user", default=None)
    forum_name = request.args.get("forum", default=None)

    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')

    if order not in ['asc', 'desc']:
        return response(3, 'Wrong order value')

    limit_str = check_limit(limit)

    since_str = check_since(since)

    if user_email:

        c, conn = connection()
        try:
            c.execute(''' select * from Thread t where t.user='{}' {} order by t.date {} {} '''.format(user_email, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_thread_dict(c, [])

        conn.close()

        return response(0, res)

    elif forum_name:

        c, conn = connection()
        try:
            c.execute(''' select * from Thread t where t.forum='{}' {} order by t.date {} {} '''.format(forum_name, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_thread_dict(c, [])

        conn.close()

        return response(0, res)
    elif forum_name and user_email:

        c, conn = connection()
        try:
            c.execute(''' select * from Thread t where t.user='{}' and t.forum='{}' {} order by t.date {} {} '''.format(user_email, forum_name, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_thread_dict(c, [])

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/listPosts/", methods=['GET'])
def list_posts_threads():

    thread_id = request.args.get("thread", type=int, default=None)
    sort = request.args.get("sort", type=str, default='flat')
    order = request.args.get("order", default='desc')
    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)

    if sort not in ['flat', 'tree', 'parent_tree']:
        return response(3, 'Wrong sort value')

    limit_str = check_limit(limit)

    if sort == 'flat':
        sort_str = 'order by p.date {} '.format(order) + limit_str
    elif sort == 'tree':
        sort_str = ''' order by SUBSTRING(path,1,8) {}, path asc '''.format(order) + limit_str
    elif sort == 'parent_tree':
        sort_str = '''order by path '''.format(order)

    if order not in ['asc', 'desc']:
        return response(3, 'Wrong order value')

    since_str = check_since(since)

    if thread_id:

        c, conn = connection()

        try:
            c.execute(''' select * from Post p where p.thread={} {} {} '''.format(thread_id, since_str, sort_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_post_dict(c, [])

        if sort == 'parent_tree':
            limit_counter = 0
            end_counter = -1
            for el in res:
                if el['parent'] is None:
                    end_counter += 1

                    if end_counter == limit:
                        break

                    limit_counter += 1
                else:
                    limit_counter += 1

            res = res[:limit_counter]

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/open/", methods=['POST'])
def open():

    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()
        try:
            c.execute(''' update Thread t set isClosed=0 where t.id={} '''.format(params['thread']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/remove/", methods=['POST'])
def remove():
    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()

        try:
            c.execute(''' update Post set isDeleted=1 where thread={} '''.format(params['thread']))
            c.execute(''' update Thread set isDeleted=1, posts=0 where id={} '''.format(params['thread']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/restore/", methods=['POST'])
def restore():

    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()

        try:
            c.execute(''' select count(*) from post where thread={} '''.format(params['thread']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        count_posts = c.fetchall()[0][0]

        try:
            c.execute(''' update Post set isDeleted=0 where thread={} '''.format(params['thread']))
            c.execute(''' update Thread set isDeleted=0, posts={} where id={} '''.format(count_posts, params['thread']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/subscribe/", methods=['POST'])
def subscribe():

    params = json.loads(request.data)

    if params['thread'] and params['user']:

        c, conn = connection()
        try:
            c.execute(''' insert into `Subscribe` (`thread`, `user`) values ('{}', '{}') '''.format(params['thread'], params['user']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        conn.close()

        res = {
            'thread': params['thread'],
            'user': params['user']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/unsubscribe/", methods=['POST'])
def unsubscribe():
    params = json.loads(request.data)

    if params['thread'] and params['user']:

        c, conn = connection()
        try:
            c.execute(''' delete from Subscribe where thread={} and user='{}' '''.format(params['thread'], params['user']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        conn.close()

        res = {
            'thread': params['thread'],
            'user': params['user']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@thread.route("/update/", methods=['POST'])
def update():
    params = json.loads(request.data)

    if params['message'] and params['slug'] and params['thread']:

        c, conn = connection()
        try:
            c.execute(''' update Thread t set t.message='{}', t.slug='{}' where t.id={} '''.format(params['message'], params['slug'], params['thread']))
            c.execute(''' select * from Thread t where t.id={} '''.format(params['thread']))
            conn.commit()
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_thread_dict(c, [])

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@thread.route("/vote/", methods=['POST'])
def vote():

    params = json.loads(request.data)

    if params['thread'] and params['vote']:

        if params['vote'] not in [-1, 1]:
            return response(3, 'Wrong vote value')

        c, conn = connection()
        try:
            if params['vote'] == -1:
                c.execute(''' update Thread t set dislikes=dislikes+1, points=points-1 where t.id={} '''.format(params['thread']))
            else:
                c.execute(''' update Thread t set likes=likes+1, points=points+1 where t.id={} '''.format(params['thread']))
            conn.commit()

            c.execute(''' select * from Thread t where t.id={} '''.format(params['thread']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_thread_dict(c, [])

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')
