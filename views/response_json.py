import json
import MySQLdb
import itertools


def connection():
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="db_kek")
    c = conn.cursor()

    return c, conn


def response(status, answer):
    resp_dict = {'code': status, 'response': answer}
    return json.dumps(resp_dict)


def true_or_false(what):
    if what == 0:
        return False
    elif what == 1:
        return True


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]


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


def fix_thread_dict(cursor):
    threads_dict = dictfetchall(cursor)
    for one_dict in threads_dict:
        one_dict['isDeleted'] = true_or_false(one_dict['isDeleted'])
        one_dict['isClosed'] = true_or_false(one_dict['isClosed'])
        one_dict['date'] = str(one_dict['date'])

    return threads_dict
