import json


def response(status, answer):
    resp_dict = {'code': status, 'response': answer}
    return json.dumps(resp_dict)
