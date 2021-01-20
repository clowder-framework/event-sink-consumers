#!/usr/bin/env python
import os
import pika
import time
import requests

# DEBUG: Remove me
#import logging
#import contextlib
#try:
#    from http.client import HTTPConnection # py3
#except ImportError:
#    from httplib import HTTPConnection # py2
#
#HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

# TODO: Read from ENV
queueName = 'event.sink'
exchangeName = 'clowder.metrics'

# FIXME: Fail-fast if no apikey is provided
amplitudeApiKey = os.getenv('AMPLITUDE_API_KEY', '') 

# Define what work to do with each message
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())

    # FIXME: Expand message to include missing required fields
    millis = int(round(time.time() * 1000))
    message = { 
      "created": millis,
      "message": body.decode(),
      "user_id": "example",
      "device_id": "example"
    }

    # TODO: Different fields here?
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    json = {
        "api_key": amplitudeApiKey,
        "events": [
            {
               # Required fields
               # FIXME: How to populate these?
               "event_type": "example",
               "user_id": os.getenv('AMPLITUDE_USER_ID', message['user_id']),
               "device_id": os.getenv('AMPLITUDE_DEVICE_ID', message['device_id']),

               # FIXME: 
               "time": message['created'],
               "event_properties": {
                   "message": message['message']
               }
            }
        ],
        "options": {
            "min_id_length": os.getenv('AMPLITUDE_MIN_ID_LENGTH', 0),
        }
    } 

    # Send POST, print response
    msg = requests.post('https://api2.amplitude.com/batch', json=json, headers=headers)
    print(msg.text)

    # Acknowledge message in RabbitMQ
    print(" [x] Done writing to Amplitude" )
    ch.basic_ack(delivery_tag = method.delivery_tag)


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare an exchange and a durable queue for our event fanout
channel.exchange_declare(exchange=exchangeName,
                         exchange_type='fanout')
channel.queue_declare(queue=queueName, durable=True)
channel.queue_bind(exchange=exchangeName, queue=queueName)

# Only fetch/work on one message at a time
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queueName,
                      on_message_callback=callback)


# Wait for messages
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


# Error-handling / clean-up
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted, cleaning up... Press Ctrl+C again to exit immediately.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    finally:
        if connection is not None:
            connection.close()

