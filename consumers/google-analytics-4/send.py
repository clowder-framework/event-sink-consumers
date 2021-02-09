#!/usr/bin/env python
import pika
import sys


message = ' '.join(sys.argv[1:]) or "Hello World!"
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
queueName = 'event.sink'
try:
    channel = connection.channel()

    channel.queue_declare(queue=queueName, durable=True)

    channel.basic_publish(exchange='',
                      routing_key=queueName,
                      body=message)

    print(" [x] Sent %r" % message)
finally:
    connection.close()
