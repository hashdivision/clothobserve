#!/bin/bash
set -e

docker pull hashdivision/clothobserve:latest
docker run -p 127.0.0.1:5000:5000 \
    -e CONFIG_OBJECT=configs.config.ProductionConfig \
    -e ROOT_PATH=/clothobserve/ \
    --restart=always \
    -d hashdivision/clothobserve:latest
