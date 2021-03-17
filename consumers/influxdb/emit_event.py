#!/usr/bin/env python
import pika
import sys
import time

# TODO: Read from ENV
queueName = 'event.sink'
exchangeName = 'clowder.metrics'

millis = int(round(time.time() * 1000))
message = ' '.join(sys.argv[1:]) or '{"created":%s,"category":"service_status","type":"up","service_name":"clowder"}' % (millis)
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
