#!/bin/bash

docker run -it --net=host --rm --env-file .env event-worker:influxdb
