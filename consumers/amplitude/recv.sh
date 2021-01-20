#!/bin/bash

docker run --net=host -e AMPLITUDE_API_KEY=${AMPLITUDE_API_KEY} -it --rm event-worker:amplitude
