#!/bin/bash
set -e

function finish {
    docker stop mongodb
    docker rm mongodb
}
trap finish EXIT

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

docker build -f Dockerfile-Test -t clothobserve-test .
docker run --name mongodb -e MONGODB_USERNAME=clothobserveadmin -e MONGODB_PASSWORD=clothobserveadmin -e MONGODB_DATABASE=clothobserve -d bitnami/mongodb:latest
docker run -it --rm --link=mongodb:mongodb -e CONFIG_OBJECT=configs.config.TestingConfig -e ROOT_PATH=/clothobserve/ -v ${PWD}/tests:/tests -v ${PWD}/docs:/docs clothobserve-test
