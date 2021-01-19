#!/bin/bash

docker run --net=host -it --rm event-worker:influxdb /usr/src/emit_event.py $@
