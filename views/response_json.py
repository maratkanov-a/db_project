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
    else:
        return what


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in cursor.fetchall()]
