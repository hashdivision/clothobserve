#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

docker-compose -f docker-compose-prod.yml pull
docker-compose -f docker-compose-prod.yml up -d
