#!/bin/bash

docker run --net=host -it --rm event-worker:google-analytics /usr/src/emit_event.py $@
