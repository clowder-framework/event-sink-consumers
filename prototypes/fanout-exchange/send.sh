#!/bin/bash

docker run --net=host -it --rm event-worker:fanout-exchange /usr/src/emit_event.py $@
