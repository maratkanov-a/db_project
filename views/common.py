from flask import Blueprint
from response_json import response

common = Blueprint('common', __name__)


# @common.route("/clear", methods=['POST'])
@common.route("/clear")
def delete_all():
    # TODO
    return response(0, 'OK')


# @common.route("/clear", methods=['GET'])
@common.route("/status")
def get_status():
    # TODO
    result = ' lalaala'
    return response(0, result)
