#!/bin/bash

docker run --net=host -it --rm event-worker:worker-queue
