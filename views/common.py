from flask import Blueprint
from response_json import *

common = Blueprint('common', __name__)


@common.route("/clear", methods=['POST'])
def delete_all():

    delete_list = ['User', 'Forum', 'Thread', 'Post', 'Follow', 'Subscribe']

    c, conn = connection()

    for el in delete_list:
        try:
            c.execute(''' delete '{}' from '{}' '''.format(el, el))
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

    conn.close()
    return response(0, 'OK')


@common.route("/status/", methods=['GET'])
def get_status():

    c, conn = connection()

    count_list = ['User', 'Forum', 'Thread', 'Post']

    count_dict = {}

    for el in count_list:
        try:
            c.execute(''' select count(*) from {} '''.format(el))
            count_dict[el] = c.fetchall()[0][0]
        except (MySQLdb.Error, MySQLdb.Warning):
            conn.close()
            return response(4, 'Unknown error')

    res = count_dict

    conn.close()

    return response(0, res)
