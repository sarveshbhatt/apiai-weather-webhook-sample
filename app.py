#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import re
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "getTMOBalance":
        return {}
   # baseurl = "https://query.t-mobile.com/v1/public/yql?"
    phone = makeYqlQuery(req)
    if phone is None:
        return {}
    res = makeWebhookResult(phone)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    msisdn = parameters.get("phone-number")
    if msisdn is None:
        return None

    return msisdn


def makeWebhookResult(data):
    # data="4257709607"
    phone = re.sub(r'\D', '', data)
    phone = phone.lstrip('1')
    phone= '{}-{}-{}'.format(phone[0:3], phone[3:6], phone[6:])
    balance =200
    balance =balance+20
    speech = "Current balance of your phone " + phone + ": is "+'${:,.2f}'.format(balance)
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
