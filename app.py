#!/usr/bin/env python

import urllib
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

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "show.florist":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    address = parameters.get("address")
    zipcode = parameters.get("zip-code")
    

    speech = "Here are the examples of FLorist A work"

    print("Response:")
    print(speech)

    kik_message = [
        {
            "type": "text",
            "body": "Here's an example of the Florist A work near " + address + ", " + zipcode
        },
        {
            "type": "picture",
            "picUrl": "http://fiorita.cz/wp-content/uploads/2017/03/kvetinarstvi-praha-jarni-kytice-tulipany-anemony-pryskyrniky.jpg"
        }
    ]

    print(json.dumps(kik_message))
    return {
        "speech": speech,
        "displayText": speech,
        "data": {"kik": kik_message},
        # "contextOut": [],
        "source": "choose-florist"
    }

    speech2 = "Here are the examples of FLorist B work"
    print ("Response:")
    print(speech2)
    
    kik_message2 = [
        {
            "type": "text",
            "body": "Here's an example of the Florist B work"
        },
        {
            "type": "picture",
            "picUrl": "http://fiorita.cz/wp-content/uploads/2017/03/spring-bouquet-jarni-kytka-web.jpg"
        }
    ]
    print(json.dumps(kik_message2))
    return {
        "speech": speech2,
        "displayText": speech2,
        "data": {"kik": kik_message2},
        "source": "choose-florist"
    }



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
