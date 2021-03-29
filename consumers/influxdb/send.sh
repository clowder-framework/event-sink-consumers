#!/bin/bash

docker run --net=host -it --rm \
  -e RABBITMQ_URI="${RABBITMQ_URI:-amqp://guest:guest@localhost/%2F}" \
  -e RABBITMQ_EXCHANGENAME="${RABBITMQ_EXCHANGENAME:-clowder.metrics}" \
  -e RABBITMQ_QUEUENAME="${RABBITMQ_QUEUENAME:-events.influxdb}" \
  event-worker:influxdb /usr/src/emit_event.py $@
