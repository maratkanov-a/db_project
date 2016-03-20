# -*- coding: utf-8 -*-
import json
import MySQLdb
from flask import Blueprint, request
from views.response_json import response, connection, dictfetchall, fix_forum_dict

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


@forum.route("/listThreads/", methods=['GET'])
def list_threads():

    forum_name = request.args.get("forum", type=str, default=None)

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

    forum_name = request.args.get("forum", type=str, default=None)

    if forum_name:
        limit = request.args.get("limit", type=int)
        order = request.args.get("order", default='desc')
        # TODO: [since_id,last_id]
        since_id = request.args.getlist('since_id')
        # TODO
        return response(0, 'good')
    else:
        return 'bad'
