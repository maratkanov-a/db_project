import json
from flask import Blueprint, request
from response_json import response, connection, dictfetchall

thread = Blueprint("thread", __name__)


def true_or_false(what):
    if what == 0:
        return False
    else:
        return True


def fix_thread_dict(cursor):
    threads_dict = dictfetchall(cursor)
    for one_dict in threads_dict:
        one_dict['isDeleted'] = true_or_false(one_dict['isDeleted'])
        one_dict['isClosed'] = true_or_false(one_dict['isClosed'])
        one_dict['date'] = str(one_dict['date'])

    return threads_dict


def fix_post_dict(cursor):
    posts_dict = dictfetchall(cursor)
    for one_dict in posts_dict:
        one_dict['isHighlighted'] = true_or_false(one_dict['isHighlighted'])
        one_dict['isApproved'] = true_or_false(one_dict['isApproved'])
        one_dict['isEdited'] = true_or_false(one_dict['isEdited'])
        one_dict['isSpam'] = true_or_false(one_dict['isSpam'])
        one_dict['isDeleted'] = true_or_false(one_dict['isDeleted'])
        one_dict['date'] = str(one_dict['date'])

    return posts_dict

@thread.route("/close", methods=['POST'])
def close():
    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()
        c.execute(''' update Thread t set isClosed=1 where t.id={} '''.format(params['thread']))

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/create", methods=['POST'])
def create():
    params = json.loads(request.data)

    if params['forum'] and params['title'] and params['isClosed'] and params['user'] and params['date'] and params[
        'message'] and params['slug']:

        if not params['isDeleted']:
            params['isDeleted'] = 0
            is_deleted = False
        else:
            params['isDeleted'] = 1
            is_deleted = True

        if params['isClosed'] == 'true':
            is_closed = 1
        else:
            is_closed = 0

        c, conn = connection()
        c.execute(
            '''insert into `Thread` (`forum`, `title`, `user`, `date`, `message`, `slug`, `isDeleted`, `isClosed`, `dislikes`, `likes`, `points`, `posts`) values ('{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') '''.format(
                params['forum'], params['title'], params['user'], params['date'], params['message'], params['slug'], params['isDeleted'],
                is_closed, 0, 0, 0, 0))
        c.execute(''' select id from Thread t where t.date='{}' '''.format(params['date']))
        res = c.fetchall()
        thread_id = res[0][0]

        response_dict = {
            'date': params['date'],
            'forum': params['forum'],
            'id': thread_id,
            'isClosed': params['isClosed'],
            "isDeleted": is_deleted,
            'message': params['message'],
            'slug': params['slug'],
            'title': params['title'],
            'user': params['user'],
        }

        conn.close()

        return response(0, response_dict)
    else:
        return response(4, 'Unknown error')


@thread.route("/details/", methods=['GET'])
def details():

    thread_id = request.args.get("thread", type=int)

    if thread_id:
        # WTF!!!!!!!!!!!!!!!!!!
        related = request.args.getlist('related')

        c, conn = connection()
        c.execute(''' select * from Thread t where t.id='{}' '''.format(thread_id))

        res = fix_thread_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/list/", methods=['GET'])
def list_threads():

    user_email = request.args.get("user", default=None)
    forum_name = request.args.get("forum", default=None)

    since = request.args.get("since", type=str, default='1981-01-01 00:00:00')
    limit = request.args.get("limit", type=int, default=None)
    order = request.args.get("order", default='desc')

    if order not in ['asc', 'desc']:
            return response(3, 'Wrong order value')

    if not limit:
            limit = 18446744073709551615

    if user_email:

        c, conn = connection()
        c.execute(''' select * from Thread t where t.user='{}' and t.date > '{}' order by t.date {} limit {} '''.format(user_email, since, order, limit))

        res = fix_thread_dict(c)

        conn.close()

        return response(0, res)

    elif forum_name:

        c, conn = connection()
        c.execute(''' select * from Thread t where t.forum='{}' and t.date > '{}' order by t.date {} limit {} '''.format(forum_name, since, order, limit))

        res = fix_thread_dict(c)

        conn.close()

        return response(0, res)
    elif user_email and user_email:

        c, conn = connection()
        c.execute(''' select * from Thread t where t.user='{}' and t.forum='{}' and t.date > '{}' order by t.date {} limit {} '''.format(user_email, forum_name, since, order, limit))

        res = fix_thread_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/listPosts/", methods=['GET'])
def list_posts_threads():

    thread_id = request.args.get("thread", type=int, default=None)
    sort = request.args.get("sort", type=str, default='flat')
    order = request.args.get("order", default='desc')
    since = request.args.get("since", type=str, default='1981-01-01 00:00:00')
    limit = request.args.get("limit", type=int, default=None)

    if sort not in ['flat', 'tree', 'parent_tree']:
        return response(3, 'Wrong sort value')

    if sort == 'flat':
        sort_str = 'order by p.date {}'.format(order)
    elif sort == 'tree':
        sort_str = 'order by p.date {}, p.path '.format(order)
    elif sort == 'parent_tree':
        sort_str = 'and p.path like order by p.date {}'.format(order)

    if order not in ['asc', 'desc']:
        return response(3, 'Wrong order value')

    if not limit:
            limit = 18446744073709551615

    if thread_id:

        c, conn = connection()
        c.execute(''' select * from Post p where p.thread={} and p.date>'{}' {} limit {} '''.format(thread_id, since, sort_str, limit))

        res = fix_post_dict(c)

        conn.close()

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/open", methods=['POST'])
def open():

    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()
        c.execute(''' update Thread t set isClosed=0 where t.id={} '''.format(params['thread']))

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/remove", methods=['POST'])
def remove():
    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()
        c.execute(''' update Thread t set isDeleted=1 where t.id={} '''.format(params['thread']))
        c.execute(''' update Post p set isDeleted=1 where p.thread={} '''.format(params['thread']))

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/restore", methods=['POST'])
def restore():
    params = json.loads(request.data)

    if params['thread']:

        c, conn = connection()
        c.execute(''' update Thread t set isDeleted=0 where t.id={} '''.format(params['thread']))
        c.execute(''' update Post p set isDeleted=0 where p.thread={} '''.format(params['thread']))

        conn.close()

        res = {
            'thread': params['thread']
        }

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/subscribe", methods=['POST'])
def subscribe():

    params = json.loads(request.data)

    if params['thread'] and params['user']:

        c, conn = connection()
        c.execute(''' insert into `Subscribe` (`thread`, `user`) values ('{}', '{}') '''.format(params['thread'], params['user']))

        conn.close()

        res = {
            'thread': params['thread'],
            'user': params['user']
        }

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/unsubscribe", methods=['POST'])
def unsubscribe():
    params = json.loads(request.data)

    if params['thread'] and params['user']:

        c, conn = connection()
        c.execute(''' delete from Subscribe where thread={} and user='{}' '''.format(params['thread'], params['user']))

        conn.close()

        res = {
            'thread': params['thread'],
            'user': params['user']
        }

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/update", methods=['POST'])
def update():
    params = json.loads(request.data)

    if params['message'] and params['slug'] and params['thread']:

        c, conn = connection()
        c.execute(''' update Thread t set message='{}', slug='{}' where t.id={} '''.format(params['message'], params['slug'], params['thread']))
        c.execute(''' select * from Thread t where t.id={} '''.format(params['thread']))

        res = fix_thread_dict(c)

        return response(0, res)
    else:
        return response(4, 'Unknown error')


@thread.route("/vote", methods=['POST'])
def vote():
    params = json.loads(request.data)

    if params['thread'] and params['vote']:

        if params['vote'] not in [-1, 1]:
            return response(3, 'Wrong vote value')

        c, conn = connection()
        if params['vote'] == -1:
            c.execute(''' update Thread t set dislikes=dislikes+1 where t.id={} '''.format(params['thread']))
        else:
            c.execute(''' update Thread t set likes=likes+1 where t.id={} '''.format(params['thread']))
        c.execute(''' select * from Thread t where t.id={} '''.format(params['thread']))

        res = res = fix_thread_dict(c)

        return response(0, res)
    else:
        return response(4, 'Unknown error')
