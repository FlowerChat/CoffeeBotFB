#!/usr/bin/env python


import urllib
import json
import os

from flask import Flask, render_template, jsonify
import requests
from key import key
from key import keyfb
import imghdr
from flask import request
from flask import make_response
#import psycopg2
import datetime
strkeyfb=str(keyfb)





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
    
    if req.get("result").get("action") == "firstfb":
        result= req.get("result")
        contexts=result.get("contexts")
        generic_con=contexts[1]

        generic_conparams=generic_con.get("parameters")
    
        facebook_id=str(generic_conparams.get("facebook_sender_id"))
        user_id_url="https://graph.facebook.com/v2.6/"+facebook_id+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAABfjhPfpDwBAEMdBzJFZAanstg21Q9cwLko70ptIUrrzuj6btRYVWZBibKVHJEIQS62DCNyYLN4FhMcP8jMtx6Ffj85ZCz22Bx0s3fM9FyP29wUZA8buvFe8lDSAhEAGPGyNwfZCjP090DkL1ZBwB5zir2TnuC2QiLm1jZAO7gFQZDZD"
        user_req=requests.get(user_id_url)
        user_json=user_req.json()
        facebook_user_firstname=user_json["first_name"]
        
        TimeStamp=str(datetime.datetime.utcnow())
        

        speech = TimeStamp
        
        print("Response:")
        print speech
        facebook_message = {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                        
                        
                        {
                            "title":"Hi, "+ facebook_user_firstname +", I can help you find the best local cafe",                            
                            "image_url":"http://www.fiorita.cz/wp-content/uploads/2017/03/kvetinarstvi-praha-jarni-kytice-tulipany-anemony-pryskyrniky.jpg",
                            "subtitle":"This bouquet was tied by my sponsors. You can order flowers through their web",
                            #}
                        
                            "buttons":[
                                {
                                    "type":"web_url",
                                    "url":"http://www.fiorita.cz",
                                    "title":"View sponsor's web"
                                                                  
                                },{                                  
                                    "type":"postback",
                                    "title":"Start Chatting",
                                    "payload":"Yes, please"
                                },{
                                    "type":"postback",
                                    "title":"Quit",
                                    "payload":"No, thanks"
                                }
                            ]              
                        }      
                        
                    ]
                }
            }
        }

        
        print(json.dumps(facebook_message))
        return {
            "data":{"facebook":facebook_message},
            "contextOut": [{"name":"facebook_location", "lifespan":0}]
        }
    
        
        
            
    elif req.get("result").get("action") == "ask.location":
        
    
        #TimeStamp=str(datetime.datetime.utcnow())
        

        #speech = TimeStamp


        print("Response:")
        #print(speech)
        

        facebook_message = {
            "text":"Great!. For better service please share your current location and I will send you info about cafes nearby",
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
            "contextOut": [{"name":"facebook_location", "lifespan":0}]
        }
    elif req.get("result").get("action")=="input.location":
        #import userloc
                
        result = req.get("result")
        contexts=result.get("contexts")
        fblocation=contexts[0]
        conparams=fblocation.get("parameters")
    
        CustLong=str(conparams.get("long"))
        CustLat=str(conparams.get("lat"))
        CustLoc=CustLat+","+CustLong
        #generic_con=contexts[3]
        generic_con=contexts[2]

        generic_conparams=generic_con.get("parameters")
    
        facebook_id=str(generic_conparams.get("facebook_sender_id"))
        user_id_url="https://graph.facebook.com/v2.6/"+facebook_id+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAABfjhPfpDwBAEMdBzJFZAanstg21Q9cwLko70ptIUrrzuj6btRYVWZBibKVHJEIQS62DCNyYLN4FhMcP8jMtx6Ffj85ZCz22Bx0s3fM9FyP29wUZA8buvFe8lDSAhEAGPGyNwfZCjP090DkL1ZBwB5zir2TnuC2QiLm1jZAO7gFQZDZD"
        user_req=requests.get(user_id_url)
        user_json=user_req.json()
        facebook_user_firstname=user_json["first_name"]
        search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        photos_url = "https://maps.googleapis.com/maps/api/place/photo"
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        amp = str("&")
        ques= str("?")
        photo_ref = str("photoreference=")
        photo_width=str("maxwidth=1600")
        key_eq=str("key=")
        key_str=str(key)
        #str_address="florist at"+str(address)
    
    #trying to retrieve pics
    
        search_payload = {"key":key, "location":CustLoc, "rankby": "distance", "type": "cafe"}
        search_req = requests.get(search_url, params=search_payload)
        search_json = search_req.json()
        gplace_id=search_json["results"][0]["place_id"]
        gplace_id2=search_json["results"][1]["place_id"]
        details_payload={"key":key, "placeid":gplace_id}
        details_payload2={"key":key, "placeid":gplace_id2}
        details_req=requests.get(details_url, params=details_payload)
        details_req2=requests.get(details_url, params=details_payload2)
        details_json=details_req.json()
        details_json2=details_req2.json()


    
   # photo id of businesses 
    
        photo_id = details_json["result"]["photos"][0]["photo_reference"]
        photo_id2=details_json2["result"]["photos"][0]["photo_reference"]
        
   # name of businesses
   
        name_shop1=details_json["result"]["name"]
        name_shop2=details_json2["result"]["name"]
        
   # addresses and tel of businesses
   
        phone_shop1=details_json["result"]["international_phone_number"]
        phone_shop2=details_json2["result"]["international_phone_number"]
        form_add1=details_json["result"]["formatted_address"]
        form_add2=details_json2["result"]["formatted_address"]
    

   


# do not remember
    
        photo_payload = {"key" : key, "maxwidth": 1600, "maxhight": 1600, "photoreference" : photo_id}
        photo_request = requests.get(photos_url, params=photo_payload)
   
    # final pictures to be shown to the user
    
        final_pic=photos_url+ques+photo_width+amp+photo_ref+photo_id+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"
        final_pic2=photos_url+ques+photo_width+amp+photo_ref+photo_id2+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"

           
        
        speech="test"
        
        
        print("Response:")
        print speech
        facebook_message = {
            "attachment": {
                "type":"image",
                "payload":{
                    "url": final_pic
                }
            }
        }
                    
                    
     #"Your current location is " + CustLong  +" " + CustLat+" hello "+facebook_user_firstname
     #   }
        print(json.dumps(facebook_message))
        return {
            "data":{"facebook":facebook_message},
            "contextOut": [{"name":"facebook_location", "lifespan":0},{"name":"generic","lifespan":0},{"name":"coffeechat","facebook_user_first":facebook_user_firstname,"lifespan":100}]
        }
    elif req.get("result").get("action")=="search.florist":
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        photos_url = "https://maps.googleapis.com/maps/api/place/photo"
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        amp = str("&")
        ques= str("?")
        photo_ref = str("photoreference=")
        photo_width=str("maxwidth=1600")
        key_eq=str("key=")
        key_str=str(key)
        str_address="florist at"+str(address)
    
    #trying to retrieve pics
    
        search_payload = {"key":key, "query":str_address, "radius": 10000}
        search_req = requests.get(search_url, params=search_payload)
        search_json = search_req.json()
        gplace_id=search_json["results"][0]["place_id"]
        gplace_id2=search_json["results"][1]["place_id"]
        details_payload={"key":key, "placeid":gplace_id}
        details_payload2={"key":key, "placeid":gplace_id2}
        details_req=requests.get(details_url, params=details_payload)
        details_req2=requests.get(details_url, params=details_payload2)
        details_json=details_req.json()
        details_json2=details_req2.json()


    
    #webadd=details_json["result"]["website"]
    #webadd_str=str(webadd)
    
        photo_id = details_json["result"]["photos"][1]["photo_reference"]
        photo_id2=details_json2["result"]["photos"][1]["photo_reference"]
        name_shop1=details_json["result"]["name"]
        name_shop2=details_json2["result"]["name"]
        phone_shop1=details_json["result"]["international_phone_number"]
        phone_shop2=details_json2["result"]["international_phone_number"]
        form_add1=details_json["result"]["formatted_address"]
        form_add2=details_json2["result"]["formatted_address"]
    

    #website0=details_json["result"]["website"]
    #website1=details_json2["result"]["website"]
    #hwebsite0="http://"+website0
    #hwebsite1="http://"+website1



    #photo_id = search_json["results"][0]["photos"][0]["photo_reference"]
    #photo_link=photos_url+"?maxwidth=1600"+"&"+"photoreference="+photo_id+"&"+key
    
        photo_payload = {"key" : key, "maxwidth": 1600, "maxhight": 1600, "photoreference" : photo_id}
        photo_request = requests.get(photos_url, params=photo_payload)
    #final_pic=str(photo_request)
    
        final_pic=photos_url+ques+photo_width+amp+photo_ref+photo_id+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"
        final_pic2=photos_url+ques+photo_width+amp+photo_ref+photo_id2+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"



        
    return {}
    

    



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
app.run(debug=True, port=port, host='0.0.0.0')