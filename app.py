# -*- coding= utf-8

from flask import Flask
from flask import request
from flask import make_response
import json
from graph import *

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
    default = {"speech": [], "displayText": [], "source": "facebook"}
    default.update(kwarg)
    return default


def facebook_data(default, **kwarg):
    """
    Messenge
    Attatchment
    quick_replies
    """

    fb = {"facebook": {}}
    fb["facebook"].update(default)
    fb["facebook"].update(kwarg)
    return fb


def facebook_location(fb_data):
    fb_data['data'].update({"quick_replies":
                            [{"content_type": "location"}]})
    return fb_data


def convert_2_api_ai_representation():
    pass


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    亞洲統神說你好。
    """
    respone = request.get_json(force=True)
    status_code = error_handle(respone)
    print "\nGets:"
    reply = True
    connections = [(Root(name=""), )]
    agent = Agent(connections=connections)
    res = default_api_ai_json(speech="亞洲統神說你好",
                              displayText="亞洲統神說你好",
                              status_code=status_code,
                              data={"facebook":
                                    {"text": text,
                                     "quick_replies": quick_replies}})

    res = json.dumps(res, indent=4)
    print "\nResponse:"
    print res
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    if reply:
        return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
