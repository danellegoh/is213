from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http
from os import environ

app = Flask(__name__)
CORS(app)

event_URL = os.environ.get('eventURL')
participant_URL = os.environ.get('participantURL')

@app.route('/join_event', methods=['POST'])
def join_event():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            participant_and_event = request.get_json()
            print("\nReceived an order in JSON:", participant_and_event)

            # do the actual work
            # 1. Send order info {cart items}
            result = processJoinEvent(participant_and_event)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
    
def processJoinEvent(participant_and_event):
    eventid = participant_and_event['eventid']
    eventtitle = participant_and_event['eventtitle']
    userEmail = participant_and_event['userEmail'] 
    # check if event exist
    event_result = invoke_http(event_URL + "/" + eventtitle, method='GET')
    
    if event_result['code'] == 404:
        return {
            "code": 404,
            "data": {
                "event_result": event_result,
        }
    }
    
    # 2. Check if participant has already signed up for this event
    else: 
        participant_result = invoke_http(participant_URL + "/" + userEmail+ "/" + str(eventid), method='POST')
        if participant_result['code'] == 404:
            return participant_result
    # 3. Else, update event in event database
        else:
            event_result = invoke_http(event_URL + "/" + eventtitle, method='PUT')
            print(event_result['message'])
            return {
                "code": 201,
                "data": {
                    "event_result": event_result,
                    "participant_result": participant_result,
                }
            }
    
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for joining events...")
    app.run(host="0.0.0.0", port=5008, debug=True)
