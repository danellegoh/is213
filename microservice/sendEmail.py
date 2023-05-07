# upon receiving input from AdminUI, retrieve emails from User (UserDB) and send necessary info to AMQP broker

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

import os
import sys

import email_amqp_setup
import requests
from invokes import invoke_http
import pika
import json

app = Flask(__name__)
CORS(app)

# URL for routing 
userURL = os.environ.get('userURL')

@app.route("/sendEmail", methods=['POST'])
def sendEmail():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # 1. receive subject and email_content from admin UI 
            info_from_ui = request.get_json()
            print("\nReceived an email in JSON:", info_from_ui)

            # 2. Retrieve emails from user DB 
            bcc = retrieveEmails()
            print(bcc)

            # 3. format email info to be sent to AMQP broker 
            # "sender" and "to" are hardcoded for the sake of the project -- sender must be an email which we have authenticated to use the API
            email = {
                "code": 201,
                "data": {
                "subject": info_from_ui["emailSubject"],
                "email_content": info_from_ui["emailBody"],
                "sender": {"name": "Ecopal", "email": "INSERT-SENDERS-EMAIL"},
                "bcc": bcc,
                "to": {"name": "Admin", "email": "INSERT-ADMIN-EMAIL"}
                }
            }

            # 3. Send email info 
            result = processSendEmail(email)

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
                "message": "sendEmail.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# def processSendEmail(email):
def processSendEmail(email):
    print("Sending the message to RabbitMQ Exchange")
    
    email_json = json.dumps(email)
    # print(email_json)

    email_amqp_setup.channel.basic_publish(exchange=email_amqp_setup.exchangename, routing_key="", 
            body=email_json, properties=pika.BasicProperties(delivery_mode = 2))

    return email_json

def retrieveEmails():
    # something wrong with invoking user microservice
    user_info = invoke_http(userURL, method='GET')
    # print(user_info)
    # return user_info
    user_data = user_info["data"]["user"]
    
    # print(user_data)
    bcc = []

    for user in user_data:
        name = user["name"]
        userEmail = user["userEmail"]
        data_to_add = {"name": name, "email": userEmail}
        bcc.append(data_to_add)
    
    return bcc

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for sending an email...")
    app.run(host="0.0.0.0", port=5009, debug=True)