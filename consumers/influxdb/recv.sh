#!/bin/bash

docker run --net=host -it --rm \
  -e RABBITMQ_URI="${RABBITMQ_URI:-amqp://guest:guest@localhost/%2F}" \
  -e RABBITMQ_EXCHANGENAME="${RABBITMQ_EXCHANGENAME:-clowder.metrics}" \
  -e RABBITMQ_QUEUENAME="${RABBITMQ_QUEUENAME:-events.influxdb}" \
  -e INFLUXDB_HOST="${INFLUXDB_HOST:-localhost}" \
  -e INFLUXDB_PORT="${INFLUXDB_PORT:-8086}" \
  -e INFLUXDB_USER="${INFLUXDB_USER:-''}" \
  -e INFLUXDB_PASSWORD="${INFLUXDB_PASSWORD:-''}" \
  -e INFLUXDB_DATABASE="${INFLUXDB_DATABASE:-clowder}" \
  -e INFLUXDB_MEASUREMENTS="${INFLUXDB_MEASUREMENTS:-events}" \
  event-worker:influxdb
