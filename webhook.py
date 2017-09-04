# -*- coding= utf-8

from flask import Flask
from flask import request
from flask import make_response
import json


app = Flask(__name__)


def error_handle(res):
    if res["status"]["code"] != 200:
        pass
    return res["status"]["code"]


def processRequest(respone):
    pass


def default_api_ai_json(**kwarg):
    """
    speech     : String  Response to the request.
    displayText: String  Text displayed on the user device screen.
    data       : Object  Additional data required for performing the action on
                        the client side. The data is sent to the client in the
                        original form and is not processed by API.AI.
    contextOut : Array of context objects

    Note: In JSON {} is object, [] is array. <3
    """
    default = {"speech": [], "displayText": [], "source": "apiai-default"}
    default.update(kwarg)
    return default


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    亞洲統神說你好。
    """
    respone = request.get_json(force=True)
    status_code = error_handle(respone)
    print "\nGets:"
    print respone
    res = default_api_ai_json(speech="亞洲統神說你好",
                              displayText="亞洲統神說你好",
                              status_code=status_code)
    res = json.dumps(res, indent=4)
    print "\nResponse:"
    print res
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
