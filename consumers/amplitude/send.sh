#!/bin/bash

docker run --net=host -it --rm event-worker:amplitude /usr/src/emit_event.py $@
