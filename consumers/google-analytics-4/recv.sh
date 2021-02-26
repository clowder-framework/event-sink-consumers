#!/bin/bash

docker run --net=host -e GOOGLE_API_SECRET=${GOOGLE_API_SECRET} -e GOOGLE_MEASUREMENT_ID=${GOOGLE_MEASUREMENT_ID} -e GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID} -it --rm event-worker:google-analytics
