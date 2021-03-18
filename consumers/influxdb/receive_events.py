#!/usr/bin/env python
import pika
import time
import json
from influxdb import InfluxDBClient

# TODO: Read from ENV
queueName = 'event.sink'
exchangeName = 'clowder.metrics'
influxHost = 'localhost'
influxPort = 8086
databaseName = 'eventsink'
measurementName = 'events'

# TODO: Credentials are needed in InfluxDB 2+

# Connect to InfluxDB
client = InfluxDBClient(host=influxHost, port=influxPort)

# Check if we need to create the database
createDB = True
databases = client.get_list_database()
for db in databases:
    if db['name'] == databaseName:
        createDB = False

if createDB:
    client.create_database(databaseName)

client.switch_database(databaseName)

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
    if ('author_id' in event):
        tags['author_id'] = event['author_id']
    if ('extractor_name' in event):
        tags['extractor_name'] = event['extractor_name']

    # Parse the rest as fields (fields are not indexed)
    if ('resource_id' in event):
        fields['resource_id'] = event['resource_id']
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
        "measurement": measurementName,
        "tags": tags,
        "time": event['created'],
        "fields": fields
    }
    client.write_points([data_point])

    print(" [x] Done writing to InfluxDB" )
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

