#!/usr/bin/env python
import os
import pika
import sys
import time

# RabbitMQ connection parameters
RABBITMQ_URI = os.getenv('RABBITMQ_URI', 'amqp://guest:guest@rabbitmq/%2F')
RABBITMQ_EXCHANGENAME = os.getenv('RABBITMQ_EXCHANGENAME', 'clowder.metrics')
RABBITMQ_QUEUENAME = os.getenv('RABBITMQ_QUEUENAME', '')

print('Using RabbitMQ: ' + str(RABBITMQ_URI))

millis = int(round(time.time() * 1000))
message = ' '.join(sys.argv[1:]) or '{"created":%s,"category":"service_status","type":"up","service_name":"clowder"}' % (millis)

connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))
try:
    channel = connection.channel()

    channel.exchange_declare(exchange=RABBITMQ_EXCHANGENAME, exchange_type='fanout', durable=True)

    channel.basic_publish(exchange=RABBITMQ_EXCHANGENAME, routing_key=RABBITMQ_QUEUENAME, body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

    print(" [x] Sent %r" % message)
finally:
    connection.close()
