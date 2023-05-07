from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import tele_amqp_setup
import requests
from invokes import invoke_http
import pika
import json 

app = Flask(__name__)
CORS(app)

event_URL = os.environ.get('eventURL')
participant_URL = os.environ.get('participantURL')

@app.route("/create_event", methods= ['POST'])
def create_event():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            event = request.get_json()
            print("\nReceived an event in JSON:", event)

            # do the actual work
            # 1. Send event info 
            result1 = processCreateEvent(event)

            return jsonify(result1), result1["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "edit_events.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
    
def processCreateEvent(event):
    # 2. Send the event info {event details}
    # Invoke the event microservice
    event_result = invoke_http(event_URL, method='POST', json=event)

    # 3. Send automated message to Telegram channel
    title = event["eventtitle"]

    newEventMessage = f"Ecopal has added a new event, {title}! Head over to the website to find out more."
    processSendMessage(newEventMessage)

    return {
        "code": 201,
        "data": {
            "event_result": event_result,
        }
    }
    
@app.route("/delete_event", methods= ['DELETE'])
def delete_event():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            event = request.get_json()
            print("\nReceived an event in JSON:", event)

            # do the actual work
            # 1. Send event info 
            # result = processDeleteEvent(event['eventtitle'])
            # return jsonify(result), result["code"]
        
            # testing new ver
            result = processDeleteEvent(event)
            return result, result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "delete_event.py internal error: " + ex_str
            }), 500
    
def processDeleteEvent(event):
    # 1. Get the event id {event details}
    # Invoke the event microservice
    eventtitle = event
    event_result = invoke_http(event_URL + "/" + eventtitle, method='GET')
    eventid = event_result['event']['eventid']
    if not eventid:
        return {
            "code": 404,
            "data": {
                "event_result": event_result,
        }
    }
    
    # 2. Delete participants from the event using eventid first
    else: 
        participant_result = invoke_http(participant_URL + "/" + str(eventid), method='DELETE')
    
    # 3. Send automated message to Telegram channel 
        deletedEventMessage = f"Ecopal is sad to announce that the event, {eventtitle} has been cancelled. Stay tuned to find out what future events we have planned."
        processSendMessage(deletedEventMessage)
        
    # 4. Delete event 

        event_result = invoke_http(event_URL + "/" + eventtitle, method='DELETE')
        print(event_result['message'])
        return {
            "code": 201,
            "data": {
                "event_result": event_result,
                "participant_result": participant_result,
            }
        }
    
@app.route("/sendEventMessage", methods=['POST'])
def sendEventMessage():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # 1. receive message_content from admin UI 
            info_from_ui = request.get_json()
            print(info_from_ui)
            print("\nReceived a message in JSON:", info_from_ui)

            # 2. Format info to be sent to AMQP broker 
            message = {
                "code": 201,
                "data": info_from_ui
            }

            # 3. Send message info 
            result = processSendMessage(message)

            print('\n------------------------')
            print('\nresult: ', result)
            return result
        
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "edit_events.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processSendMessage(message):
    print("Sending the message to RabbitMQ Exchange")
    
    event_json = json.dumps(message)
    print(event_json)

    tele_amqp_setup.channel.basic_publish(exchange=tele_amqp_setup.exchangename, routing_key="", 
            body=event_json, properties=pika.BasicProperties(delivery_mode = 2))

    return event_json

    
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for editing events...")
    app.run(host="0.0.0.0", port=5007, debug=True)
