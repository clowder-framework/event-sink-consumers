#!/bin/bash
# Build all Docker images

set -e

cd consumers/
cd echo/ && docker build -t event-worker:echo . ; cd ../
cd mongodb/ && docker build -t event-worker:mongodb . ; cd ../
cd ../

# Build all prototype Docker images
cd prototypes/
cd send-recv/ && docker build -t event-worker:send-recv . ; cd ../
cd worker-queue/ && docker build -t event-worker:worker-queue . ; cd ../
cd fanout-exchange/ && docker build -t event-worker:fanout-exchange . ; cd ../
cd ../
