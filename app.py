#!/usr/bin/env python


import urllib
import json
import os

from flask import Flask, render_template, jsonify
import requests
from key import key
import imghdr
from flask import request
from flask import make_response
#import psycopg2
import datetime






#str = unicode(str, errors='ignore')


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
    
    if req.get("result").get("action") == "input.welcome":
        
    
        TimeStamp=str(datetime.datetime.utcnow())
        

     
    

    

        speech = TimeStamp


        print("Response:")
        print(speech)

        facebook_message = {
            "text":"For better service please share your current location:",
            "quick_replies":[
                {
                    "content_type":"location",
                }
            ]
        }
        

        print(json.dumps(facebook_message))
        return {
            #"speech": speech,
            #"displayText": speech,
            "data": {"facebook": facebook_message},
        # "contextOut": [],
            "contextOut": [{"name":"facebook_location", "lifespan":5}]
        }
    elif req.get("result").get("action")=="input.location":
        result = req.get("result")
        contexts=result.get("contexts")
        fblocation=contexts[0]
        conparams=fblocation.get("parameters")
    
        CustLong=str(conparams.get("long"))
        CustLat=str(conparams.get("lat"))
        speech="test"
        
        
        print("Response:")
        print speech
        facebook_message = {
            "text": "Your current location is " + CustLong  +" " + CustLat
        }
        print(json.dumps(facebook_message))
        return {
            "data":{"facebook":facebook_message},
            "contextOut": [{"name":"facebook_location", "lifespan":5}]
        }

        
    return {}
    

    



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
app.run(debug=True, port=port, host='0.0.0.0')