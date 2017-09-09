# -*- coding= utf-8

from flask import Flask
from flask import request
from flask import make_response
import json
from lawrence_utils.utils import find_resturant_nearby, geocoding
from lawrence_utils.utils import find_resturant_by_type
import uniout
import pprint
import numpy as np
import os
import subprocess
import urllib2

app = Flask(__name__)


def print_dict(input_dict):
    pprint.pprint(input_dict)



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


def counter_how_many(respone):
    for cntx in respone['result']['contexts']:
        if cntx['name'] == "finded":
            kw = cntx['parameters'].get("counter", None)
            if kw is None:
                cntx['parameters']["counter"] = 0
            else:
                cntx['parameters'].update(("counter",
                                        cntx["parameters"]["counter"]+1))
            context_out = cntx
            counter = cntx["parameters"]["counter"]
            return context_out, counter
    return respone['result']['contexts'], 0

def check_info(respone):
    for context in respone['result']['contexts']:
        if context['name'] == 'restaurant':
            return context['parameters']['location'] and \
                (context['parameters']['type'] or \
                 context['parameters']['anytype'])
        return False

from httplib import HTTPSConnection
import requests


APIAI_TOKEN = "e32492590c2e4258b7bc5d2f2f7b5f64"


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """
    亞洲統神說你好。
    """

    respone = request.get_json(force=True)
    status_code = error_handle(respone)
    print "\nGets:"
    print_dict(respone)

    p = {'event': { 'name': 'restaurant_finded', 'data': {'name': 'Sam'}},
         'lang': 'en', "sessionId": respone["sessionId"],
         'timezone':'America/New_York'}

    api_ai_connect = HTTPSConnection

    print respone['result']['action']
    data = {}
    speech = respone['result']['fulfillment']['speech']
    act = respone['result']['action']
    ## 記喜歡或不喜歡的counter
    context_out, counter = counter_how_many(respone)

    # check actions
    if respone['result']['action'] == "query.user_loc_fb":
        data["facebook"] = {"text": respone['result']["fulfillment"]['speech'],
                            "quick_replies": [{"content_type": "location"}]}

    elif act == "query.both" or check_info(respone):
        type_response = respone['result']['parameters']

        if type_response['type']:
            type_ = type_response['type']

        elif type_response['anytype']:
            type_ = type_response['anytype']
        type_ = "".join(type_).encode("utf-8")

        T = all([context['name'] != "facebook_location" \
             for context in respone['result']['contexts']])

        if T:
            loc_name = respone['result']['parameters']['location'].values()
            loc_name = loc_name[0].encode("utf-8")
            loc_xy = geocoding(loc_name)

            try:
                random = np.random.choice(range(5))
                print loc_xy
                restatuarant_spec = find_resturant_nearby(keywords=type_,
                                                        counter=0,
                                                        lat=loc_xy[0],
                                                        lon=loc_xy[1])
                #restatuarant_spec = find_resturant_by_type(
                #    keywords= type_ + " " + loc_name,
                #    counter=counter)

                data['facebook'] = {"attachment":{ "type": "template",
                                            "payload":
                                            {"template_type": "open_graph",
                                            "elements":[
                                                {"url": restatuarant_spec['link'],
                                                    "buttons":[{"type":"web_url",
                                                                "url": restatuarant_spec['link'],
                                                                "title":restatuarant_spec['title']}]}]
                                            }
                                            }
                                }
            except IndexError:
                speech = "亞洲統神覺得這裡太荒涼了。"
        else:
            try:
                loc_xy = respone['originalRequest']['data']['postback']['data']
                restatuarant_spec = find_resturant_nearby(keywords=type_,
                                                        counter=0,
                                                        lat=loc_xy['lat'],
                                                        lon=loc_xy['long'])
                data['facebook'] = {"attachment":{ "type": "template",
                                                "payload":
                                                {"template_type": "open_graph",
                                                "elements":[
                                                    {"url": restatuarant_spec['link'],
                                                        "buttons":[{"type":"web_url",
                                                                    "url": restatuarant_spec['link'],
                                                                    "title":restatuarant_spec['title']}]}]
                                                 }
                                                  }
                                    }
            except IndexError:
                speech = "RRR~找不到啊~吃7-11啊"

    elif act == "query.loc":
        loc_name = respone['result']['parameters']['location'].values()
        loc_name = loc_name[0].encode("utf-8")
        loc_xy = geocoding(loc_name)

        try:
            restatuarant_spec = find_resturant_nearby(lat=loc_xy[0], lon=loc_xy[1],
                                                    counter=counter)

            data['facebook'] = {"attachment":{ "type": "template",
                                          "payload":
                                          {"template_type": "open_graph",
                                           "elements":[
                                               {"url": restatuarant_spec['link'],
                                                "buttons":[{"type":"web_url",
                                                            "url": restatuarant_spec['link'],
                                                            "title":restatuarant_spec['title']}]}]
                                           }
                                          }
                            }
        except IndexError:
            speech = "亞洲統神覺得這裡太荒涼了。"

    elif act == "query.type":
        type_response = respone['result']['parameters']
        if type_response['type']:
            type_ = type_response['type']

        elif type_response['anytype']:
            type_ = type_response['anytype']
        try:
            restatuarant_spec = find_resturant_by_type(
                counter=counter, keywords="".join(type_).encode('utf-8'))
            pprint.pprint(restatuarant_spec)

            data['facebook'] = {"attachment":{ "type": "template",
                                            "payload":
                                            {"template_type": "open_graph",
                                            "elements":[
                                                {"url": restatuarant_spec['link'],
                                                    "buttons":[{"type":"web_url",
                                                                "url": restatuarant_spec['link'],
                                                                "title":restatuarant_spec['title']}]}]
                                            }
                                            }
                                }

        except IndexError:
            speech = "{}種類可能比較少人吃喔。".format(type_)

    elif act == "query.nearby":
        try:
            loc_xy = respone['originalRequest']['data']['postback']['data']
            restatuarant_spec = find_resturant_nearby(counter=0,lat=loc_xy['lat'],
                                                    lon=loc_xy['long'])
            data['facebook'] = {"attachment":{ "type": "template",
                                            "payload":
                                            {"template_type": "open_graph",
                                            "elements":[
                                                {"url": restatuarant_spec['link'],
                                                    "buttons":[{"type":"web_url",
                                                                "url": restatuarant_spec['link'],
                                                                "title":restatuarant_spec['title']}]}]
                                            }
                                            }
                                }
        except IndexError:
            speech = "RRRRR找不到啊~滑滑滑"

    res = default_api_ai_json(speech=speech,
                              displayText=speech,
                              status_code=status_code,
                              data=data,
                              followEvent={"name": "restaurant_fined",
                                           "data":{"test":"empty"}})

    res_ = json.dumps(res, indent=4)
    print "\nResponse:"
    pprint.pprint(res)
    r = make_response(res_)
    r.headers['Content-Type'] = 'application/json'
    print p
    import os, sys
    os.system(r'''curl -X POST -H "Content-Type: application/json; charset=utf-8" -H "Authorization: Bearer e32492590c2e4258b7bc5d2f2f7b5f64" --data "{'event':{ 'name': 'restaurant_finded', 'data': {'name': 'Sam'}}, 'timezone':'America/New_York', 'lang':'en', 'sessionId':'241ec822-b357-46a8-afb3-9a261cf55e3e'}" "https://api.api.ai/api/query?v=20150910"''')
    req = requests.post(url="https://api.api.ai/api/query?v=20150910",
                        data=p,
                  headers={"Authorization": "Bearer {}".format(APIAI_TOKEN),
                           "Content-Type": "application/json; charset=utf-8"})
    print req.text


    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
