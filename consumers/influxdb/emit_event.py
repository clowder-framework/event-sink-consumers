#!/usr/bin/env python
import pika
import sys

# TODO: Read from ENV
queueName = 'event.sink'
exchangeName = 'clowder.metrics'

message = ' '.join(sys.argv[1:]) or "Hello World!"
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
try:
    channel = connection.channel()

    channel.exchange_declare(exchange=exchangeName, exchange_type='fanout', durable=True)

    channel.basic_publish(exchange=exchangeName, routing_key='', body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

    print(" [x] Sent %r" % message)
finally:
    connection.close()
