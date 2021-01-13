#!/bin/bash

docker run --net=host -it --rm event-worker:mongodb /usr/src/emit_event.py $@
