#!/usr/bin/env python
import os
import pika
import time
import requests
import json

# TODO: Read from ENV
queueName = 'event.sink'
exchangeName = 'clowder.metrics'

# FIXME: Fail-fast if no apikey is provided
GoogleApiSecret = os.getenv('GOOGLE_API_SECRET', '') 
GoogleMeasurementId = os.getenv('GOOGLE_MEASUREMENT_ID', '')
GoogleClientId = os.getenv('GOOGLE_CLIENT_ID','')

# Define what work to do with each message
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())

    # FIXME: Expand message to include missing required fields
    millis = int(round(time.time() * 1000))
    message = { 
      "created": millis,
      "message": body.decode(),
      "client_id": "example",
    }

    # TODO: Different fields here?
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "*/*",
    }

    params = {
        "api_secret": GoogleApiSecret,
        "measurement_id": GoogleMeasurementId,
    }
    
    event_json = {
        "client_id": os.getenv('GOOGLE_CLIENT_ID', message['client_id']),
        "events": [
            {
               # Required fields
               "name": "test_event",
               "params": {
                   "message": message['message']
               }
            }
        ],
        }

    # Send POST, print response
    msg = requests.post('https://google-analytics.com/mp/collect', params=params, json=event_json, headers=headers)
    print(msg.text)

    # Acknowledge message in RabbitMQ
    print(" [x] Done writing to Google Analytics" )
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

