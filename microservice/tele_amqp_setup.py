import pika
from os import environ

# hostname = "localhost" # default hostname
# port = 5672 # default port

hostname = environ.get('rabbit_host') or 'localhost' ###
port = environ.get('rabbit_port') or 5672

# connect to broker 
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=hostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600, # these parameters to prolong the expiration time (in seconds) of the connection
))
    
channel = connection.channel()
# Set up the exchange if the exchange doesn't exist
# using 'fanout' exchange to send to all queues
exchangename="message_fanout"
exchangetype="fanout"
channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)

# all queues can be found below 

############   Message queue   #############
#delcare Message queue
queue_name = 'Message'
channel.queue_declare(queue=queue_name, durable=True) 

#bind Message queue
## no routing key since fanout exchange 
channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='') 
    

# function to set up connection and channel to a local AMQP broker 

def check_setup():
    global connection, channel, hostname, port, exchangename, exchangetype

    if not is_connection_open(connection):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, heartbeat=3600, blocked_connection_timeout=3600))
    if channel.is_closed:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True)


def is_connection_open(connection):
    try:
        connection.process_data_events()
        return True
    except pika.exceptions.AMQPError as e:
        print("AMQP Error:", e)
        print("...creating a new connection.")
        return False