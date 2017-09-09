# -*- coding= utf-8

from flask import Flask
from flask import request
from flask import make_response
import json
from lawrence_utils.utils import find_resturant_nearby

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
    print respone
    print respone['result']['action']
    data = {}
    speech = respone['result']['fulfillment']['speech']
    act = respone['result']['action']
    if respone['result']['action'] == "query.user_loc_fb":
        data["facebook"] = {"text": respone['result']["fulfillment"]['speech'],
                            "quick_replies": [{"content_type": "location"}]
                            }

    if respone['result']['action'] == "query.restaurant_near_by":
        respone[""]

    elif act == "query.both":
        type_response = respone['']
        loc = respone['']

    elif act == "query.loc":
        pass

    elif act == "query.type":
        type_response = respone['result']['parameters']
        if type_response['type'] is not None:
            type_ = type_response['type']
        elif type_response['anytype'] is not None:
            speech = 'OIJFOIJF'


    elif act == "query.nearby":
        loc_xy = respone['originalRequest']['data']['postback']['data']
        restatuarant_spec = find_resturant_nearby(**loc_xy)
        data['facebook'] = {"attachment":{ "type": "template",
                                          "payload":
                                          {"template_type": "open_graph",
                                           "elements":[
                                               {"url": restatuarant_spec['url'],
                                                "buttons":[{"type":"web_url",
                                                            "url": restatuarant_spec['url'],
                                                            "title":restatuarant_spec['title']}]}]
                                           }
                                          }
                            }

    res = default_api_ai_json(speech=speech,
                              displayText=speech,
                              status_code=status_code,
                              data=data)

    res = json.dumps(res, indent=4)
    print "\nResponse:"
    print res
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
