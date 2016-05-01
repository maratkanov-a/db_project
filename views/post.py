# -*- coding: utf-8 -*-
import json
import MySQLdb
from flask import Blueprint, request
from views.response_json import *

post = Blueprint("post", __name__)


@post.route("/create/", methods=['POST'])
def create():
    params = json.loads(request.data)

    if params['date'] and params['thread'] and params['message'] and params['user'] and params['forum']:

        is_approved = params.get('isHighlighted', False)
        is_highlighted = params.get('isHighlighted', False)
        is_edited = params.get('isEdited', False)
        is_spam = params.get('isSpam', False)
        is_deleted = params.get('isHighlighted', False)

        if not params.get('parent', None):
            params['parent'] = 'Null'

        c, conn = connection()

        try:
            c.execute(
                ''' insert into `Post` (`thread`, `user`, `forum`, `date`, `message`, `dislikes`, `likes`, `points`, `parent`, `isHighlighted`, `isApproved`, `isEdited`, `isSpam`, `isDeleted`) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}) '''.format(
                    params['thread'], params['user'], params['forum'], params['date'], params['message'], 0, 0, 0,
                    params['parent'], is_highlighted, is_approved, is_edited, is_spam, is_deleted))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        c.execute(''' select * from Post p where p.date='{}' '''.format(params['date']))

        res = fix_post_dict(c, [])

        conn.close()

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@post.route("/details/", methods=['GET'])
def details():

    post_id = request.args.get("post", type=int, default=None)
    related = request.args.getlist('related', type=str)

    if post_id:

        c, conn = connection()

        try:
            c.execute(''' select * from Post p where p.id='{}' '''.format(post_id))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        if c.rowcount == 0:
            return response(1, 'Not Found')

        res = fix_post_dict(c, related)

        conn.close()

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@post.route("/list/", methods=['GET'])
def list_posts():

    forum_name = request.args.get("forum", type=str, default=None)
    thread_id = request.args.get("thread", type=int, default=None)

    since = request.args.get("since", type=str, default=None)
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')

    if order not in ['asc', 'desc']:
        return response(3, 'Wrong order value')

    limit_str = check_limit(limit)

    since_str = check_since(since)

    if thread_id:

        c, conn = connection()
        try:
            c.execute(''' select * from Post p where p.thread='{}' {} order by p.date {} {} '''.format(thread_id, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_post_dict(c, [])

        conn.close()

        return response(0, res)

    elif forum_name:

        c, conn = connection()
        try:
            c.execute(''' select * from Post p where p.forum='{}' {} order by p.date {} {} '''.format(forum_name, since_str, order, limit_str))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_post_dict(c, [])

        conn.close()

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@post.route("/remove/", methods=['POST'])
def remove():

    params = json.loads(request.data)

    if params['post']:

        c, conn = connection()

        try:
            c.execute(''' update Post p set p.isDeleted=1 where p.id={} '''.format(params['post']))
            c.execute(''' select thread from Post where id={} '''.format(params['post']))
            id_thread = c.fetchall()[0][0]
            c.execute(''' update Thread set posts=posts-1 where id={} '''.format(id_thread))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        conn.close()

        res = {
            'post': params['post']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@post.route("/restore/", methods=['POST'])
def restore():
    params = json.loads(request.data)

    if params['post']:
        c, conn = connection()

        try:
            c.execute(''' update Post p set p.isDeleted=0 where p.id={} '''.format(params['post']))
            c.execute(''' select thread from Post where id={} '''.format(params['post']))
            id_thread = c.fetchall()[0][0]
            c.execute(''' update Thread set posts=posts+1 where id={} '''.format(id_thread))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

        conn.close()

        res = {
            'post': params['post']
        }

        return response(0, res)
    else:
        return response(2, 'Invalid request')


@post.route("/update/", methods=['POST'])
def update():
    params = json.loads(request.data)

    if params['post'] and params['message']:

        c, conn = connection()
        try:
            c.execute(''' update Post p set p.message='{}' where p.id={} '''.format(params['message'], params['post']))
            c.execute(''' select * from Post p where p.id={} '''.format(params['post']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_post_dict(c, [])

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')


@post.route("/vote/", methods=['POST'])
def vote():
    params = json.loads(request.data)

    if params['post'] and params['vote']:

        if params['vote'] not in [-1, 1]:
            return response(3, 'Wrong vote value')

        c, conn = connection()
        try:
            if params['vote'] == -1:
                c.execute(''' update Post p set dislikes=dislikes+1, points=points-1 where p.id={} '''.format(params['post']))
            else:
                c.execute(''' update Post p set likes=likes+1, points=points+1 where p.id={} '''.format(params['post']))
            conn.commit()

            c.execute(''' select * from Post p where p.id={} '''.format(params['post']))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(1, 'Not Found')

        res = fix_post_dict(c, [])

        return response(0, res[0])
    else:
        return response(2, 'Invalid request')
