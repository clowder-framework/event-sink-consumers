#!/usr/bin/env python
import os
import pika
import time
import json
from influxdb import InfluxDBClient

# RabbitMQ connection parameters
RABBITMQ_URI = os.getenv('RABBITMQ_URI', 'amqp://guest:guest@rabbitmq/%2F')
RABBITMQ_EXCHANGENAME = os.getenv('RABBITMQ_EXCHANGENAME', 'clowder.metrics')
RABBITMQ_QUEUENAME = os.getenv('RABBITMQ_QUEUENAME', 'event.sink')

print('Using RabbitMQ: ' + str(RABBITMQ_URI))

# InfluxDB connection parameters
INFLUXDB_HOST = os.getenv('INFLUXDB_HOST', 'localhost')
INFLUXDB_PORT = os.getenv('INFLUXDB_PORT', 8086)

INFLUXDB_USER = os.getenv('INFLUXDB_USER', '')
INFLUXDB_PASSWORD = os.getenv('INFLUXDB_PASSWORD', '')

INFLUXDB_DATABASE = os.getenv('INFLUXDB_DATABASE', 'clowder')
INFLUXDB_MEASUREMENT = os.getenv('INFLUXDB_MEASUREMENT', 'events')

# Connect to InfluxDB
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT, username=INFLUXDB_USER, password=INFLUXDB_PASSWORD, database=INFLUXDB_DATABASE)

# Check if we need to create the database
client.create_database(INFLUXDB_DATABASE)
client.switch_database(INFLUXDB_DATABASE)

# Define what work to do with each message
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())

    event = json.loads(body.decode()) 

    tags = {}
    fields = {}

    # Parse tags first (tags are indexed, cardinality must be < 100K)
    if ('type' in event):
        tags['type'] = event['type']
    if ('category' in event):
        tags['category'] = event['category']
    if ('user_id' in event):
        tags['user_id'] = event['user_id']
    if ('healthy' in event):
        tags['healthy'] = event['healthy']
    if ('author_id' in event):
        tags['author_id'] = event['author_id']
    if ('extractor_name' in event):
        tags['extractor_name'] = event['extractor_name']

    # Parse the rest as fields (fields are not indexed)
    if ('resource_id' in event):
        fields['resource_id'] = event['resource_id']
    if ('response_time_avg' in event):
        fields['response_time_avg'] = event['response_time_avg']
    if ('response_time_min' in event):
        fields['response_time_min'] = event['response_time_min']
    if ('response_time_max' in event):
        fields['response_time_max'] = event['response_time_max']
    if ('response_time_loss' in event):
        fields['response_time_loss'] = event['response_time_loss']
    if ('uptime' in event):
        fields['uptime'] = event['uptime']
    if ('dataset_id' in event):
        fields['dataset_id'] = event['dataset_id']
    if ('service_name' in event):
        fields['service_name'] = event['service_name']
    if ('dataset_name' in event):
        fields['dataset_name'] = event['dataset_name']
    if ('author_name' in event):
        fields['author_name'] = event['author_name']
    if ('user_name' in event):
        fields['user_name'] = event['user_name']
    if ('resource_name' in event):
        fields['resource_name'] = event['resource_name']
    if ('size' in event):
        fields['size'] = event['size']

    # Write event as a data point in InfluxDB
    data_point = {
        "measurement": INFLUXDB_MEASUREMENT,
        "tags": tags,
        "time": event['created'],
        "fields": fields
    }
    client.write_points([data_point])

    print(" [x] Done writing to InfluxDB" )
    ch.basic_ack(delivery_tag = method.delivery_tag)


# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URI))
channel = connection.channel()

# Declare an exchange and a durable queue for our event fanout
channel.exchange_declare(exchange=RABBITMQ_EXCHANGENAME,
                         exchange_type='fanout',
                         durable=True)
channel.queue_declare(queue=RABBITMQ_QUEUENAME, durable=True)
channel.queue_bind(exchange=RABBITMQ_EXCHANGENAME, queue=RABBITMQ_QUEUENAME)

# Only fetch/work on one message at a time
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=RABBITMQ_QUEUENAME,
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

