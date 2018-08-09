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

docker build -f Dockerfile-Quicktest -t clothobserve-quicktest .
docker run --link=mongodb:mongodb \
    -e CONFIG_TYPE=TestingConfig \
    -e ROOT_PATH=/clothobserve/ \
    -e MONGODB_PORT=27017 \
    -v ${PWD}/clothobserve:/clothobserve \
    -v ${PWD}/tests:/tests \
    -it --rm clothobserve-quicktest