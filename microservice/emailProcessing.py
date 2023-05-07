from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

import json
import os 
import email_amqp_setup

def receiveMessage():
    email_amqp_setup.check_setup()

    queue_name = 'Email'

    # set up consumer 
    email_amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    email_amqp_setup.channel.start_consuming() 
    # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):
    print("\nReceived an email to be sent by " + __file__)
    message = json.loads(body)
    processMessage(message)
    sendMessage(message)
    print() # print a new line feed

def processMessage(message):
    print("Received message to be sent:")
    print(message)

def sendMessage(message):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = 'INSERT-API-KEY'

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    data = message["data"]

    subject = data["subject"]
    html_content = "<html><body><p>" + data["email_content"] + "</p></body></html>"
    sender = data["sender"]
    to = [data["to"]]
    bcc = data["bcc"]

    # print statements for troubleshooting
    # print("data:")
    # print(data)
    # print()
    # print("to:")
    # print(to)
    # print()
    # print("bcc:")
    # print(bcc)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)

    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

if __name__ == "__main__":  
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": in exchange '{}' ...".format(email_amqp_setup.exchangename))
    receiveMessage()
