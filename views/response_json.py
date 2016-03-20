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


def fix_post_dict(cursor, related):
    posts_dict = dictfetchall(cursor)
    for one_dict in posts_dict:
        user = one_dict['user']
        one_dict['isHighlighted'] = true_or_false(one_dict['isHighlighted'])
        one_dict['isApproved'] = true_or_false(one_dict['isApproved'])
        one_dict['isEdited'] = true_or_false(one_dict['isEdited'])
        one_dict['isSpam'] = true_or_false(one_dict['isSpam'])
        one_dict['isDeleted'] = true_or_false(one_dict['isDeleted'])
        one_dict['date'] = str(one_dict['date'])

        if 'user' in related and cursor.execute(''' select * from User u where u.email='{}' '''.format(user)):
            user_dict = fix_user_dict(cursor)
            one_dict['user'] = user_dict[0]

        if 'forum' in related:
            forum = one_dict['forum']
            if cursor.execute('''select * from Forum f where f.short_name='{}' '''.format(forum)):
                forum_dict = fix_forum_dict(cursor, [])
                one_dict['forum'] = forum_dict

        if 'thread' in related and cursor.execute('''select * from Thread t where t.user='{}' '''.format(user)):
            thread_dict = fix_thread_dict(cursor, [])
            one_dict['thread'] = thread_dict[0]

    return posts_dict


def fix_thread_dict(cursor, related):
    threads_dict = dictfetchall(cursor)
    for one_dict in threads_dict:
        user = one_dict['user']
        one_dict['isDeleted'] = true_or_false(one_dict['isDeleted'])
        one_dict['isClosed'] = true_or_false(one_dict['isClosed'])
        one_dict['date'] = str(one_dict['date'])

        if 'user' in related and cursor.execute(''' select * from User u where u.email='{}' '''.format(user)):
            user_dict = fix_user_dict(cursor)
            one_dict['user'] = user_dict[0]

        if 'forum' in related:
            forum = one_dict['forum']
            if cursor.execute('''select * from Forum f where f.short_name='{}' '''.format(forum)):
                forum_dict = fix_forum_dict(cursor, [])
                one_dict['forum'] = forum_dict

    return threads_dict


def fix_user_dict(cursor):

    user_dict = dictfetchall(cursor)
    for one_dict in user_dict:
        one_dict['isAnonymous'] = true_or_false(one_dict['isAnonymous'])

        cursor.execute('''select f.follower from Follow f where f.followee = '{}' '''.format(one_dict['email']))
        user_followers = cursor.fetchall()
        cursor.execute('''select f.followee from Follow f where f.follower = '{}' '''.format(one_dict['email']))
        user_following = cursor.fetchall()
        cursor.execute(''' select s.thread from Subscribe s where s.user='{}' '''.format(one_dict['email']))
        user_subscriptions = cursor.fetchall()

        one_dict['followers'] = [email[0] for email in user_followers]
        one_dict['following'] = [email[0] for email in user_following]
        one_dict['subscriptions'] = [subs[0] for subs in user_subscriptions]
    return user_dict


def fix_forum_dict(cursor, related):
    forum_dict = dictfetchall(cursor)[0]
    if 'user' in related:
        user = forum_dict['user']
        cursor.execute(''' select * from User u where u.email='{}' '''.format(user))
        user_dict = fix_user_dict(cursor)[0]
        forum_dict['user'] = user_dict
    return forum_dict


def check_limit(limit):
    if limit:
        return 'limit {}'.format(limit)
    else:
        return ''


def check_since(since):
    if since:
        return ''' and date > '{}' '''.format(since)
    else:
        return ''


