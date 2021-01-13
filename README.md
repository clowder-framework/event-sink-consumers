## Clowder event-sink

A centralized place where Clowder can submit metrics data. A RabbitMQ fanout exchange is used to route events to the correct queue or queues. A set of workers watch the queues they are interested in and operate on the events one at a time as they are queued up.

## Consumers
Each consumer subdirectory has the same structure:
* 2 Python files => one sender and one receiver (specific to each prototype)
* `Dockerfile` => produces Docker image
* `requirements.txt` => Python dependencies
* `build.sh` => uses the above files to build and tag the Docker image
* `recv.sh` => runs the Docker image to listen for messages
* `send.sh` => runs the Docker image to send a message


### Echo

Python files:
* Sender: `emit_event.py`
* Receiver: `receive_events.py`

A nearly full example that creates an exchange with `type=fanout`, creates a durable queue, and binds the queue to the exchange. The sender can then send to the exchange while the listeners subscribe to the queue(s) beneath.

This consumer simply echoes the sender's message back in the listener's console. In addition, if the message contains any `.` characters, the worker will wait 1 second for each `.` present in the message.

### MongoDB

Python files:
* Sender: `emit_event.py`
* Receiver: `receive_events.py`

A nearly full example that creates an exchange with `type=fanout`, creates a durable queue, and binds the queue to the exchange. The sender can then send to the exchange while the listeners subscribe to the queue(s) beneath.

This consumer pushes the sender's message to a pre-configure database/collection within MongoDB.


## Prototypes
Each prototype subdirectory has the same structure as the Consumers above.

To run a prototype, you will first need to build its Docker image.
All can be built simultaneously by running `./build-all.sh` in the root directory.
To rebuild a single prototype, you can run `./build.sh` in the appropriate subdirectory.

After building an image, you will need at least two terminal windows open to the same directory:
* In all terminals except for one, run `./recv.sh` to listen.
* In the last terminal, run `./send.sh This is only a test` to send a test message.

You should see the sender's message appear in the consoles of the listeners!


### send-recv

Python files:
* Sender: `send.py`
* Receiver: `receive.py`

A basic send/receive pattern testing out the creating durable queues.

This prototype simply echoes the sender's message back in the listener's console with no special handling based on the message contents.


### worker-queue

Python files:
* Sender: `new_task.py`
* Receiver: `worker.py`

A slightly more complex worker that creates durable queues and send persistent messages.

This prototype echoes the sender's message back in the listener's console. In addition, if the message contains any `.` characters, the worker will wait 1 second for each `.` present in the message.


### fanout-exchange

Python files:
* Sender: `emit_event.py`
* Receiver: `receive_events.py`

A nearly full example that creates an exchange with `type=fanout`, creates a durable queue, and binds the queue to the exchange. The sender can then send to the exchange while the listeners subscribe to the queue(s) beneath.

This prototype echoes the sender's message back in the listener's console. In addition, if the message contains any `.` characters, the worker will wait 1 second for each `.` present in the message.
