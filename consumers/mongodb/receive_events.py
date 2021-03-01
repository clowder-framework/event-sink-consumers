#!/usr/bin/env python
import pika
import time
from pymongo import MongoClient

# TODO: Read from ENV
queueName = 'event.sink'
exchangeName = 'clowder.metrics'
mongoHost = 'localhost'
mongoPort = 27017
databaseName = 'clowder'
collectionName = 'eventsink.messages'

# Connect to MongoDB
client = MongoClient(mongoHost, mongoPort)
db = client[databaseName]
collection = db[collectionName]

# Define what work to do with each message
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    millis = int(round(time.time() * 1000))
    message = { "created": millis, "message": body.decode() }
    collection.insert_one(message)
    print(" [x] Done writing to MongoDB" )
    ch.basic_ack(delivery_tag = method.delivery_tag)


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare an exchange and a durable queue for our event fanout
channel.exchange_declare(exchange=exchangeName,
                         exchange_type='fanout',
                         durable=True)
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

