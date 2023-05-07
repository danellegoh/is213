import tele_amqp_setup
import requests
import json 
import os

# define variables 
BOT_TOKEN = 'INSERT-TELEBOT-TOKEN'

## we will have a general channel for all updates related to Ecopal Events 
CHAT_ID = '@INSERT-CHANNEL-NAME'

def receiveMessage():
    tele_amqp_setup.check_setup()

    queue_name = 'Message'

    # set up consumer 
    tele_amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    tele_amqp_setup.channel.start_consuming() 
    # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body):
    print("\nReceived a message to be sent by " + __file__)
    message = json.loads(body)
    processMessage(message)
    broadcastMessage(message)
    print() # print a new line feed

def processMessage(message):
    print("Received message to be sent:")
    print(message)

def broadcastMessage(message):
    # message_content = f'Ecopal has a new event for you! \n\n{message["eventtitle"]} \n{message["eventdescription"]} \n{message["eventdate"]} \n{message["starttime"]} \n{message["endtime"]}' 
    
    if type(message) == str:
        message_content = message
    
    else:
        message_content = message["data"]["message"]

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    data = {'chat_id': CHAT_ID, 'text': message_content}

    response = requests.post(url, json=data)
    print(response.json())

if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": in exchange '{}' ...".format(tele_amqp_setup.exchangename))
    receiveMessage()
