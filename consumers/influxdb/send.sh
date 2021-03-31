#!/bin/bash

docker run --net=host -it --rm --env-file .env event-worker:influxdb /usr/src/emit_event.py $@
