#!/bin/bash
set -e

function finish {
    docker stop mongodb
    docker rm mongodb
}
trap finish EXIT

docker pull hashdivision/clothobserve:development
docker run --name mongodb -e MONGODB_USERNAME=clothobserveadmin -e MONGODB_PASSWORD=clothobserveadmin -e MONGODB_DATABASE=clothobserve -d bitnami/mongodb:latest
docker run -it --rm --link=mongodb:mongodb -e CONFIG_OBJECT=configs.config.TestingConfig -e ROOT_PATH=/clothobserve/ -v tests:/tests -v docs:/docs hashdivision/clothobserve:development
