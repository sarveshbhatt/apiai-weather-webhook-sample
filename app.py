#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

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
    baseurl = "https://query.t-mobile.com/v1/public/yql?"
    phone = makeYqlQuery(req)
    if phone is None:
        return {}
#yql_url = baseurl + urlencode({'q': phone}) + "&format=json"
     #    result = urlopen(yql_url).read()
   #  data = json.loads(result)
   # res = makeWebhookResult(data)
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
   # query = data.get('query')
   # if query is None:
 #       return {}

  #  result = query.get('results')
  #  if result is None:
   #     return {}

#    channel = result.get('channel')
  #  if channel is None:
  #      return {}

 #   item = channel.get('item')
  #  location = channel.get('location')
    #units = channel.get('units')
    #if (location is None) or (item is None) or (units is None):
    #    return {}

   # condition = item.get('condition')
  #  if condition is None:
  #      return {}

    # print(json.dumps(item, indent=4))
    
    speech = "Current balance of your phone " + data + ": is $200" 

   # speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
      #       ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

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
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
