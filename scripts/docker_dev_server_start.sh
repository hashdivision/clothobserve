#!/bin/bash
set -e

function finish {
    docker stop mongodb
    docker rm mongodb
}
trap finish EXIT

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

docker run --name mongodb \
    -e MONGODB_USERNAME=clothobserveadmin \
    -e MONGODB_PASSWORD=clothobserveadmin \
    -e MONGODB_DATABASE=clothobserve \
    -d bitnami/mongodb:latest

docker build -f Dockerfile-Dev-Server -t clothobserve-dev-server .
docker run -p 127.0.0.1:43597:5000 \
    -e CONFIG_TYPE=DevelopmentServerConfig \
    -e ROOT_PATH=/clothobserve/ \
    -e MONGODB_PORT=27017 \
    -d clothobserve-dev-server
