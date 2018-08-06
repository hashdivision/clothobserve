#!/bin/bash
set -e

if [ -z "$1" ] ; then
    echo "Usage: $0 feature_name"
	exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

git fetch origin
git checkout -b "feature-$1" development
git push -u origin HEAD
echo "$1" > FEATURE
git add FEATURE
git commit -m "Creates feature branch for feature $1"
git push
