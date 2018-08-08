#!/bin/bash
set -e

if [ -z "$1" ] ; then
    echo "Usage: $0 release_version"
	exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

git pull origin development
git checkout -b "release-$1" development
git push -u origin HEAD
echo "$1" > VERSION
git add VERSION
git commit -m "Creates release branch for version $1"
git push
