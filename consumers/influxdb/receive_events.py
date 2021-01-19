#!/usr/bin/env python
import pika
import time
from influxdb import InfluxDBClient

# TODO: Read from ENV
queueName = 'event.sink'
exchangeName = 'clowder.metrics'
influxHost = 'localhost'
influxPort = 8086
databaseName = 'eventsink'

# Connect to MongoDB
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

    millis = int(round(time.time() * 1000))
    message = { "created": millis, "message": body.decode() }

    # TODO: Different measurements here?
    data_points = [{
        "measurement": "events",
        "tags": {
            "user": "User",
            "resourceId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": message['created'],
        "fields": {
            "message": message['message']
        }
    }] 
    client.write_points(data_points)

    print(" [x] Done writing to InfluxDB" )
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

