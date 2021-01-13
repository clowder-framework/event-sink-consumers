#!/bin/bash

docker run --net=host -it --rm event-worker:echo /usr/src/emit_event.py $@
